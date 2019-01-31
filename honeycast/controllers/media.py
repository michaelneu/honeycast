from ..log import logger
from .base import BaseController
from pychromecast.controllers.media import TYPE_GET_STATUS, TYPE_MEDIA_STATUS, TYPE_LOAD

NS_MEDIA = "urn:x-cast:com.google.cast.media"

class MediaController(BaseController):
    def __init__(self):
        super().__init__(NS_MEDIA)

    def get_reply(self, message):
        message_type = message.data.get("type", "")

        if message_type == TYPE_GET_STATUS:
            return self.create_default_reply(message, {
                "type": TYPE_MEDIA_STATUS,
                "status": {},
            })
        elif message_type == TYPE_LOAD:
            media = message.data.get("media", {})
            content = media.get("contentId", "")
            mime = media.get("contentType", "")

            if media:
                logger.info("playing %s (%s)", media, mime)

        return super().get_reply(message)
