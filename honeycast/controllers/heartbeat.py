from .base import BaseController
from pychromecast.socket_client import NS_HEARTBEAT, TYPE_PING, TYPE_PONG

class HeartbeatController(BaseController):
    def __init__(self):
        super().__init__(NS_HEARTBEAT)

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == TYPE_PING:
            return self.create_default_reply(message, {
                "type": TYPE_PONG,
            })

        return super().get_reply(message)
