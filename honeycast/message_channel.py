import socket
import ssl
import socketserver
import logging
from http.server import BaseHTTPRequestHandler
from struct import pack, unpack
from multiprocessing import Process

import json

import cast_channel_pb2

logger = logging.getLogger("honeycast-message-channel")

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

class MessageChannelSSLServer(socketserver.TCPServer):
    def get_request(self):
        sock, from_addr = self.socket.accept()
        ssl_sock = ssl.wrap_socket(sock, keyfile="key.pem",
                certfile="cert.pem", server_side=True)
        return ssl_sock, from_addr

class MessageChannelHandler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        sock = self.request

        while True:
            packet_size, = unpack(">I", recvall(sock, 4))

            data = recvall(sock, packet_size)

            cast_request = cast_channel_pb2.CastMessage()
            cast_request.ParseFromString(data)

            print("Received: ", cast_request)

            cast_response = cast_channel_pb2.CastMessage()
            cast_response.protocol_version = cast_response.CASTV2_1_0
            cast_response.source_id = cast_request.destination_id
            cast_response.destination_id = cast_request.source_id
            cast_response.payload_type = cast_channel_pb2.CastMessage.STRING
            cast_response.namespace = "urn:x-cast:com.google.cast.tp.heartbeat"
            cast_data = { 'type': "PING" }
            cast_response.payload_utf8 = json.dumps(cast_data, ensure_ascii=False)

            print("Sending: ", cast_response)

            sock.sendall(pack(">I", cast_response.ByteSize()) +
                    cast_response.SerializeToString())
        

class MessageChannel:
    def __init__(self, address="127.0.0.1", port=None):
        self.msgchd = MessageChannelSSLServer((address, port), MessageChannelHandler);
        self._msgchd = Process(target=self.msgchd.handle_request)

    def start(self):
        self._msgchd.start()

    def stop(self):
        self._msgchd.terminate()
        self._msgchd.join()
