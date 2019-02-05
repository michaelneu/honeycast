from .controllers import Message
from .controllers.connection import ConnectionController
from .controllers.heartbeat import HeartbeatController
from .controllers.media import MediaController
from .controllers.receiver import ReceiverController
from .controllers.spotify import SpotifyController
from .log import logger
from pychromecast.cast_channel_pb2 import CastMessage
import json
import logging
import socket
import ssl
import struct

def unpack_uint(buffer):
    return struct.unpack(">I", buffer)[0]

def pack_uint(value):
    return struct.pack(">I", value)

class CastException(Exception):
    def __init__(self, message):
        self.message = message

class CastServer:
    def __init__(self, key_path, cert_path, port=8009, tcp_backlog=100):
        raw_socket = socket.socket()
        self._socket = ssl.wrap_socket(raw_socket, keyfile=key_path, certfile=cert_path, server_side=True)
        self._socket.bind(("0.0.0.0", port))
        self._socket.listen(tcp_backlog)
        logger.info("started cast server on port %d", port)

    def close(self):
        self._socket.close()

    def get_client(self):
        client_socket, address = self._socket.accept()
        logger.info("client connected at %s", str(address))
        return CastClient(client_socket)

    def run(self):
        while True:
            try:
                client = self.get_client()
                while True:
                    try:
                        client.receive_and_reply_once()
                    except CastException as ex:
                        logger.warning("exception in cast client: %s", ex.message)
                        break
            except KeyboardInterrupt:
                break

class CastClient:
    def __init__(self, socket):
        self._socket = socket
        self._controllers = [
            HeartbeatController(),
            ConnectionController(),
            ReceiverController(),
            MediaController(),
            SpotifyController(),
        ]

    def close(self):
        self._socket.close()

    def _receive_message(self):
        size_bytes = self._socket.recv(4)

        if not size_bytes:
            raise CastException("could not receive message size")

        size = unpack_uint(size_bytes)
        logger.debug("about to receive %d bytes", size)

        cast_message_bytes = self._socket.recv(size)

        if not cast_message_bytes:
            raise CastException("could not receive message")

        cast_message = CastMessage()
        cast_message.ParseFromString(cast_message_bytes)

        message = self._parse_message(cast_message)
        logger.debug("received %s", str(message))
        return message

    def _parse_message(self, message):
        payload_raw = message.payload_utf8
        data = json.loads(payload_raw)
        return Message(source_id=message.source_id, destination_id=message.destination_id, namespace=message.namespace, data=data)

    def _send_message(self, message):
        logger.debug("sending %s", str(message))

        cast_message = CastMessage()
        cast_message.protocol_version = cast_message.CASTV2_1_0
        cast_message.source_id = message.source_id
        cast_message.destination_id = message.destination_id
        cast_message.payload_type = CastMessage.STRING
        cast_message.namespace = message.namespace
        cast_message.payload_utf8 = json.dumps(message.data)

        size = cast_message.ByteSize()
        size_bytes = pack_uint(size)
        cast_message = cast_message.SerializeToString()

        try:
            self._socket.send(size_bytes + cast_message)
        except:
            raise CastException("could not send message")

    def receive_and_reply_once(self):
        message = self._receive_message()
        replies = [controller.get_reply(message) for controller in self._controllers if controller.matches(message.namespace)]

        if len(replies) > 0:
            reply = replies[0]

            if reply:
                self._send_message(reply)
