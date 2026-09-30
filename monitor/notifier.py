import logging

import requests

logger = logging.getLogger("twitch-monitor")


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
