import os
import asyncio
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)
logger = logging.getLogger("twitch-monitor")


class Config:
    """Carrega e valida as configurações a partir das variáveis de ambiente."""

    def __init__(self):
        self.client_id = os.environ.get("TWITCH_CLIENT_ID")
        self.client_secret = os.environ.get("TWITCH_CLIENT_SECRET")
        self.topico_ntfy = os.environ.get("TOPICO_NTFY", "bot_twitch")
        self.intervalo = int(os.environ.get("INTERVALO_SEGUNDOS", 60))
        self.porta = int(os.environ.get("PORT", 8080))
        self.streamers = self._carregar_streamers()

    def _carregar_streamers(self) -> list[str]:
        """Lê os canais a monitorar.

        Aceita uma lista separada por vírgula em STREAMERS
        (ex.: "cellbit,gaules,loud_coringa") ou, por compatibilidade,
        o valor único em STREAMER_NOME.
        """
        brutos = os.environ.get("STREAMERS")
        if not brutos:
            brutos = os.environ.get("STREAMER_NOME", "cellbit")

        nomes = [nome.strip().lower() for nome in brutos.split(",") if nome.strip()]
        # Remove duplicados preservando a ordem.
        return list(dict.fromkeys(nomes))

    def validar(self) -> None:
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "TWITCH_CLIENT_ID e TWITCH_CLIENT_SECRET precisam estar definidos."
            )
        if not self.streamers:
            raise ValueError("Nenhum streamer configurado para monitorar.")


class Notifier:
    """Responsável por enviar notificações para o ntfy.sh."""

    def __init__(self, topico: str):
        self.url = f"https://ntfy.sh/{topico}"

    def enviar(self, titulo: str, mensagem: str) -> None:
        try:
            requests.post(
                self.url,
                data=mensagem.encode("utf-8"),
                headers={
                    "Title": titulo,
                    "Tags": "video_game,bell",
                },
                timeout=10,
            )
        except requests.RequestException as erro:
            logger.error("Falha ao enviar notificação: %s", erro)


class KeepAliveServer:
    """Servidor HTTP mínimo para evitar a hibernação do serviço no Render."""

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self._responder()
            self.wfile.write(b"Bot da Twitch Online e operando!")

        def do_HEAD(self):
            self._responder()

        def _responder(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

        def log_message(self, *args):
            # Silencia os logs padrão do HTTPServer.
            pass

    def __init__(self, porta: int):
        self.porta = porta

    def iniciar(self) -> None:
        servidor = HTTPServer(("0.0.0.0", self.porta), self._Handler)
        thread = threading.Thread(target=servidor.serve_forever, daemon=True)
        thread.start()
        logger.info("Keep-alive server rodando na porta %s", self.porta)


class StreamerState:
    """Encapsula o estado de monitoramento de um único streamer."""

    def __init__(self, nome: str):
        self.nome = nome
        self.user_id: str | None = None
        self.online = False
        self.jogo_atual: str | None = None


class TwitchStreamMonitor:
    """Orquestra o monitoramento de um ou mais canais da Twitch."""

    def __init__(self, config: Config, notifier: Notifier):
        self.config = config
        self.notifier = notifier
        self.estados = {nome: StreamerState(nome) for nome in config.streamers}
        self.twitch: Twitch | None = None

    async def _conectar(self) -> None:
        self.twitch = await Twitch(self.config.client_id, self.config.client_secret)
        logger.info("Conectado à Twitch API.")

    async def _resolver_usuarios(self) -> None:
        """Resolve os IDs dos streamers configurados; remove os inexistentes."""
        logins = list(self.estados.keys())
        async for user in self.twitch.get_users(logins=logins):
            estado = self.estados.get(user.login.lower())
            if estado:
                estado.user_id = user.id

        nao_encontrados = [
            nome for nome, estado in self.estados.items() if estado.user_id is None
        ]
        for nome in nao_encontrados:
            logger.warning("Streamer não encontrado, será ignorado: %s", nome)
            del self.estados[nome]

    def _notificar(self, titulo: str, mensagem: str) -> None:
        logger.info(mensagem)
        self.notifier.enviar(titulo, mensagem)

    async def _verificar_streamer(self, estado: StreamerState) -> None:
        stream = await first(self.twitch.get_streams(user_id=estado.user_id))

        if stream:
            jogo_atual = stream.game_name
            if not estado.online:
                self._notificar(
                    f"Monitor: {estado.nome}",
                    f"{estado.nome} está ONLINE!!\n Jogando: {jogo_atual}",
                )
                estado.online = True
                estado.jogo_atual = jogo_atual
            elif jogo_atual != estado.jogo_atual:
                self._notificar(
                    f"Monitor: {estado.nome}",
                    f"{estado.nome} trocou de jogo!!.\n Novo jogo: {jogo_atual}",
                )
                estado.jogo_atual = jogo_atual
        else:
            if estado.online:
                self._notificar(
                    f"Monitor: {estado.nome}",
                    f"{estado.nome} encerrou a live.",
                )
                estado.online = False
                estado.jogo_atual = None

    async def executar(self) -> None:
        await self._conectar()
        await self._resolver_usuarios()

        if not self.estados:
            logger.error("Nenhum streamer válido para monitorar. Encerrando.")
            await self.twitch.close()
            return

        logger.info(
            "Bot iniciado! Monitorando: %s", ", ".join(self.estados.keys())
        )

        try:
            while True:
                for estado in list(self.estados.values()):
                    try:
                        await self._verificar_streamer(estado)
                    except Exception as erro:
                        logger.error(
                            "Erro ao verificar %s: %s", estado.nome, erro
                        )
                await asyncio.sleep(self.config.intervalo)
        except KeyboardInterrupt:
            logger.info("Monitoramento encerrado pelo usuário.")
        finally:
            await self.twitch.close()


def main() -> None:
    config = Config()
    config.validar()

    KeepAliveServer(config.porta).iniciar()

    notifier = Notifier(config.topico_ntfy)
    monitor = TwitchStreamMonitor(config, notifier)
    asyncio.run(monitor.executar())


if __name__ == "__main__":
    main()
