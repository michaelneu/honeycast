from ..config import config
from .base import BaseController
from pychromecast.socket_client import NS_RECEIVER, TYPE_GET_STATUS, TYPE_RECEIVER_STATUS
import uuid

class ReceiverController(BaseController):
    def __init__(self):
        super().__init__(NS_RECEIVER)
        self._session_id = str(uuid.uuid4())

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == TYPE_GET_STATUS:
            return self.create_default_reply(message, {
                "requestId": message.data.get("requestId", 0),
                "type": TYPE_RECEIVER_STATUS,
                "status": {
                    "applications": [
                        {
                            "appId": "CC1AD845",
                            "displayName": "Default Media Receiver",
                            "iconUrl": "",
                            "isIdleScreen": False,
                            "launchedFromCloud": False,
                            "namespaces": [
                                {
                                    "name": "urn:x-cast:com.google.cast.cac"
                                },
                                {
                                    "name": "urn:x-cast:com.google.cast.broadcast"
                                },
                                {
                                    "name": "urn:x-cast:com.google.cast.media"
                                }
                            ],
                            "sessionId": self._session_id,
                            "statusText": "Default Media Receiver",
                            "transportId": self._session_id
                        }
                    ],
                    "userEq": {
                        "high_shelf": {
                            "frequency": config.get("device.sound.equalizer.high_shelf.frequency", 4500.0),
                            "gain_db": config.get("device.sound.equalizer.high_shelf.gain_db", -2.0),
                            "quality": config.get("device.sound.equalizer.high_shelf.quality", 0.707),
                        },
                        "low_shelf": {
                            "frequency": config.get("device.sound.equalizer.low_shelf.frequency", 150.0),
                            "gain_db": config.get("device.sound.equalizer.low_shelf.gain_db", 3.0),
                            "quality": config.get("device.sound.equalizer.low_shelf.quality", 0.707),
                        },
                        "max_peaking_eqs": 0,
                        "peaking_eqs": []
                    },
                    "volume": {
                        "controlType": "master",
                        "level": config.get("device.sound.volume.level", 0.1),
                        "muted": config.get("device.sound.volume.muted", False),
                        "stepInterval": config.get("device.sound.volume.step_interval", 0.2)
                    }
                },
            })

        return super().get_reply(message)
