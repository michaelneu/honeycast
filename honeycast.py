import socket
import threading
import logging
import socketserver
import json

from uuid import uuid4 as random_uuid
from zeroconf import ServiceInfo, Zeroconf
from http.server import BaseHTTPRequestHandler

addr = "127.0.0.1"
port = 5000
cast_status_port = 8008

class HoneyCastHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/setup/eureka_info?options=detail":
            json_payload = json.dumps({ 
                "name": "ThisIsName", 
                "detail": {
                    "model_name": "ThisIsModelName", 
                    "manufacturer": "JJ" 
                }
            })

            self.send_response(200, json_payload)
        else:
            print("Not implemented? %s" % self.path)
            self.send_response(200, "OK")
        self.end_headers()

    def do_POST(self):
        print(self.path)
        self.send_response(200, "OK")
        self.end_headers()

def handle_request(stop_event, server):
    server.timeout = 1
    while not stop_event.wait(0):
        server.handle_request()

class HoneyCast():
    """HoneyCast main collection"""

    def __init__(self):
        self.logger = logging.getLogger("HoneyCast")

    def start_honeypot_service(self, device_name):
        desc = { 
                "md": "model_name_placeholder", 
                "id": str(random_uuid()), 
                "fn": device_name 
               }

        self.honeycast = ServiceInfo("_googlecast._tcp.local.", 
                "Honeycast Service._googlecast._tcp.local.",
                socket.inet_aton(addr), port, 0, 0, desc)

        self.logger.info("Opening socket at %i" % port)

        self.httpd = socketserver.TCPServer((addr, cast_status_port), HoneyCastHandler)
        self.httpd_stop_event = threading.Event()
        self.httpd_thread = threading.Thread(target = handle_request, 
                                             args = (self.httpd_stop_event, self.httpd))
        self.httpd_thread.start()

        # Start socket here

        self.logger.info("Creating zeroconf service broadcast")
        self.zeroconf = Zeroconf()
        self.zeroconf.register_service(self.honeycast)

        self.logger.info("Started a fake cast device with name %s" % device_name)

    def stop_honeypot_service(self):
        self.zeroconf.unregister_service(self.honeycast)
        self.zeroconf.close()
        self.httpd_stop_event.set()
        self.httpd_thread.join()

