import os


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
