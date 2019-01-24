import socket
import logging
from zeroconf import ServiceInfo, Zeroconf

logger = logging.getLogger("honeycast-discovery")

class Discovery:
    def __init__(self, address="127.0.0.1", port=None, description=None):
        service_type = "_googlecast._tcp.local."
        service_name = "HoneyCast Service." + service_type
        address_bytes = socket.inet_aton(address)

        self._zeroconf = None
        self._service = ServiceInfo(service_type, service_name, address_bytes, port, properties=description)

    def start(self):
        if self._zeroconf is not None:
            return

        logger.info("starting discovery")

        self._zeroconf = Zeroconf()
        self._zeroconf.register_service(self._service)

    def stop(self):
        if self._zeroconf is None:
            return

        logger.info("stopping discovery")

        self._zeroconf.unregister_service(self._service)
        self._zeroconf.close()
        self._zeroconf = None
