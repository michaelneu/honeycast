from ..log import logger
from .base import BaseController
from pychromecast.controllers.spotify import APP_NAMESPACE, APP_SPOTIFY
from spotipy import Spotify

class SpotifyController(BaseController):
    @classmethod
    def app_information(cls, session_id):
        return [
            {
                "appId": cls.app_id(),
                "displayName": "Spotify",
                "iconUrl": "",
                "isIdleScreen": False,
                "launchedFromCloud": False,
                "namespaces": [
                    {
                        "name": "urn:x-cast:com.spotify.chromecast.secure.v1"
                    },
                ],
                "sessionId": session_id,
                "statusText": "Spotify",
                "transportId": session_id
            }
        ]

    @classmethod
    def app_id(cls):
        return APP_SPOTIFY

    def __init__(self):
        super().__init__(APP_NAMESPACE)
        self._spotify = None

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == "setCredentials":
            token = message.data.get("credentials", "")
            logger.debug("received spotify token %s", token)

            self._spotify = Spotify(auth=token)
            user = self._spotify.me()
            no_value = "[n/a]"
            email = user.get("email", no_value)
            name = user.get("display_name", no_value)
            country = user.get("country", no_value)
            birthday = user.get("birthdate", no_value)
            logger.info("%s (%s from %s, born %s) launched spotify", email, name, country, birthday)

        return super().get_reply(message)
