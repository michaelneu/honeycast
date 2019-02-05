from ..log import logger
from .base import BaseController
from pychromecast.controllers.spotify import APP_NAMESPACE
from spotipy import Spotify
import pdb

class SpotifyController(BaseController):
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
