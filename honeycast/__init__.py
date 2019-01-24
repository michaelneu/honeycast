from multiprocessing import Process
import socket
import logging
import json

from uuid import uuid4 as random_uuid
from zeroconf import ServiceInfo, Zeroconf
from http.server import BaseHTTPRequestHandler

from web import httpd

addr = "127.0.0.1"
port = 5000
cast_status_port = 8008

class HoneyCast():
    """HoneyCast main collection"""

    def __init__(self):
        self.logger = logging.getLogger("HoneyCast")

    def start_honeypot_service(self, device_name):
        desc = {
            "md": "model_name_placeholder",
            "id": str(random_uuid()),
            "fn": device_name,
        }

        self.honeycast = ServiceInfo("_googlecast._tcp.local.",
                "Honeycast Service._googlecast._tcp.local.",
                socket.inet_aton(addr), port, 0, 0, desc)

        self.logger.info("Opening socket at %i" % port)

        self.httpd = Process(target=httpd.run, kwargs={ "port": cast_status_port })
        self.httpd.start()

        # Start socket here

        self.logger.info("Creating zeroconf service broadcast")
        self.zeroconf = Zeroconf()
        self.zeroconf.register_service(self.honeycast)

        self.logger.info("Started a fake cast device with name %s" % device_name)

    def stop_honeypot_service(self):
        self.zeroconf.unregister_service(self.honeycast)
        self.zeroconf.close()

        self.httpd.terminate()
        self.httpd.join()


if __name__ == "__main__":
    honeycast = HoneyCast()
    honeycast.start_honeypot_service("")
