import socket
import logging
from struct import unpack
from multiprocessing import Process

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
    def handle(self):
        sock = self.request
        packet_size = unpack(">I", recvall(sock, 4))

        data = recvall(sock, packet_size)

        cast_message = cast_channel_pb2.CastMessage()
        cast_message.ParseFromString(data)

        device_auth_message = cast_channel_pb2.DeviceAuthMessage()
        device_auth_message.ParseFromString(cast_message.payload_binary)

        auth_response = cast_channel_pb2.AuthResponse()

        sock.sendall(pack(">I", auth_response.ByteSize()) +
                auth_response.SerializeToString())

        pdb.set_trace()

class MessageChannel:
    def __init__(self, address="127.0.0.1", port=None):
        self.msgchd = MessageChannelSSLServer((address, port), MessageChannelHandler);
        self._msgchd = Process(target=self.msgchd.handle_request)

    def start(self):
        self._msgchd.start()

    def stop(self):
        self._msgchd.terminate()
        self._msgchd.join()
