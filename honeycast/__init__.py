from web import httpd
from discovery import Discovery
from multiprocessing import Process
from uuid import uuid4 as random_uuid
import logging

addr = "127.0.0.1"
port = 5000
cast_status_port = 8008

class HoneyCast():
    """HoneyCast main collection"""

    def __init__(self, device_name):
        self._logger = logging.getLogger("HoneyCast")
        self._device_name = device_name

        self._httpd = Process(target=httpd.run, kwargs={ "port": cast_status_port })
        self._discovery = Discovery(addr, port, {
            "md": "model_name_placeholder",
            "id": str(random_uuid()),
            "fn": device_name,
        })

    def start_honeypot_service(self):
        self._httpd.start()
        self._discovery.start()
        self._logger.info("Opening socket at %i" % port)

        # Start socket here

        self._logger.info("Started a fake cast device with name %s", self._device_name)

    def stop_honeypot_service(self):
        self._discovery.stop()
        self._httpd.terminate()
        self._httpd.join()


if __name__ == "__main__":
    honeycast = HoneyCast("")
    honeycast.start_honeypot_service()
