from . import Message
from uuid import uuid4

class BaseController:
    @classmethod
    def app_id(cls):
        return None

    @classmethod
    def app_information(cls, session_id):
        return []

    def __init__(self, namespace):
        self._namespace = namespace
        self._session_id = str(uuid4())

    def matches(self, namespace):
        return self._namespace == namespace

    def create_default_reply(self, message, data):
        return Message(source_id=message.destination_id, destination_id=message.source_id, namespace=message.namespace, data=data)

    def get_reply(self, message):
        return None
