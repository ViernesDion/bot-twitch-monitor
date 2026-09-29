import os
import logging
import requests
import asyncio
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first

logging.basicConfig(
    level=logging.INFO
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)

class TwitchStreamMonitor:
    def __(self, streamer_nome: str):
