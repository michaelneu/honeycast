from ..config import config
from ..log import logger
from .base import BaseController
from pychromecast.socket_client import NS_RECEIVER, TYPE_GET_STATUS, TYPE_RECEIVER_STATUS, TYPE_LAUNCH
import uuid

class ReceiverController(BaseController):
    def __init__(self):
        super().__init__(NS_RECEIVER)
        self._session_id = str(uuid.uuid4())
        self._app_id = None

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == TYPE_GET_STATUS:
            return self.create_default_reply(message, {
                "requestId": message.data.get("requestId", 0),
                "type": TYPE_RECEIVER_STATUS,
                "status": {
                    "applications": [
                        {
                            "appId": self._app_id or "CC1AD845",
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
        elif message_type == TYPE_LAUNCH:
            app_id = message.data.get("appId", None)
            logger.info("launching app %s", app_id)
            self._app_id = app_id

            return self.create_default_reply(message, {
                "requestId": message.data.get("requestId", 0),
                "type": TYPE_RECEIVER_STATUS,
                "status": {
                    "applications": [
                        {
                            "appId": self._app_id or "CC1AD845",
                            "displayName": "Default Media Receiver",
                            "iconUrl": "",
                            "isIdleScreen": False,
                            "launchedFromCloud": False,
                            "namespaces": [
                                {
                                    "name": "urn:x-cast:com.spotify.chromecast.secure.v1"
                                },
                            ],
                            "sessionId": self._session_id,
                            "statusText": "Default Media Receiver",
                            "transportId": self._session_id
                        }
                    ],
                }
            })

        return super().get_reply(message)
