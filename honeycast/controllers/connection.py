from .base import BaseController
from pychromecast.socket_client import NS_CONNECTION

class ConnectionController(BaseController):
    def __init__(self):
        super().__init__(NS_CONNECTION)

    def get_reply(self, message):
        return None
