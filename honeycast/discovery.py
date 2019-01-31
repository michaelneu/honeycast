from .config import config
from .log import logger
from zeroconf import ServiceInfo, Zeroconf
import socket

class Discovery:
    def __init__(self, zeroconf_name="", address="127.0.0.1", port=None, model_name="", uuid="", device_name=""):
        service_type = "._googlecast._tcp.local."
        service_name = zeroconf_name + service_type
        address_bytes = socket.inet_aton(address)

        self._zeroconf = None
        self._service = ServiceInfo(service_type, service_name, address_bytes, port, properties={
            "md": model_name,
            "id": uuid,
            "fn": device_name,
        })

    def run(self):
        if self._zeroconf is not None:
            return

        logger.info("starting discovery")

        try:
            self._zeroconf = Zeroconf()
            self._zeroconf.register_service(self._service)
        except KeyboardInterrupt:
            pass

    def stop(self):
        if self._zeroconf is None:
            return

        logger.info("stopping discovery")

        self._zeroconf.unregister_service(self._service)
        self._zeroconf.close()
        self._zeroconf = None
