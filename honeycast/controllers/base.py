from . import Message

class BaseController:
    def __init__(self, namespace):
        self._namespace = namespace

    def matches(self, namespace):
        return self._namespace == namespace

    def create_default_reply(self, message, data):
        return Message(source_id=message.destination_id, destination_id=message.source_id, namespace=message.namespace, data=data)

    def get_reply(self, message):
        return None
