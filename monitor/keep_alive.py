import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger("twitch-monitor")


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
