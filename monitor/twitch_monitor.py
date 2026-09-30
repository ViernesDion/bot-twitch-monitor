import asyncio
import logging

from twitchAPI.twitch import Twitch
from twitchAPI.helper import first

from .config import Config
from .notifier import Notifier
from .streamer_state import StreamerState

logger = logging.getLogger("twitch-monitor")


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
