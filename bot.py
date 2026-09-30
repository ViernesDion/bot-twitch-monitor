import asyncio
import logging

from monitor import Config, KeepAliveServer, Notifier, TwitchStreamMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)


def main() -> None:
    config = Config()
    config.validar()

    KeepAliveServer(config.porta).iniciar()

    notifier = Notifier(config.topico_ntfy)
    monitor = TwitchStreamMonitor(config, notifier)
    asyncio.run(monitor.executar())


if __name__ == "__main__":
    main()
