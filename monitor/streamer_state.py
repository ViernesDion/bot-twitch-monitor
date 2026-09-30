class StreamerState:
    """Encapsula o estado de monitoramento de um único streamer."""

    def __init__(self, nome: str):
        self.nome = nome
        self.user_id: str | None = None
        self.online = False
        self.jogo_atual: str | None = None
