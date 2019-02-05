from ..config import config
from ..log import logger
from .base import BaseController
from pychromecast.socket_client import NS_RECEIVER, TYPE_GET_STATUS, TYPE_RECEIVER_STATUS, TYPE_LAUNCH
from uuid import uuid4

class ReceiverController(BaseController):
    @classmethod
    def app_information(cls, session_id):
        return [
            {
                "appId": cls.app_id(),
                "displayName": "Default Media Receiver",
                "iconUrl": "",
                "isIdleScreen": False,
                "launchedFromCloud": False,
                "namespaces": [
                    {
                        "name": "urn:x-cast:com.google.cast.cac",
                    },
                    {
                        "name": "urn:x-cast:com.google.cast.broadcast",
                    },
                    {
                        "name": "urn:x-cast:com.google.cast.media",
                    },
                ],
                "sessionId": session_id,
                "statusText": "Default Media Receiver",
                "transportId": session_id,
            },
        ]

    @classmethod
    def app_id(cls):
        return "CC1AD845"

    def __init__(self):
        super().__init__(NS_RECEIVER)
        self._session_id = str(uuid4())
        self._launched_app_id = None

    def _get_application_field(self):
        for controller in BaseController.__subclasses__():
            if controller.app_id() == self._launched_app_id:
                return controller.app_information(self._session_id)

    def _create_status_from_message(self, message):
        application_field = self._get_application_field() or self.app_information(self._session_id)

        return self.create_default_reply(message, {
            "requestId": message.data.get("requestId", 0),
            "type": TYPE_RECEIVER_STATUS,
            "status": {
                "applications": application_field,
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

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == TYPE_GET_STATUS:
            return self._create_status_from_message(message)
        elif message_type == TYPE_LAUNCH:
            app_id = message.data.get("appId", None)
            logger.info("launching app %s", app_id)
            self._launched_app_id = app_id
            return self._create_status_from_message(message)

        return super().get_reply(message)
