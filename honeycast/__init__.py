from .web import httpd
from .discovery import Discovery
from .message_channel import MessageChannel
from multiprocessing import Process
from uuid import uuid4 as random_uuid
import logging
import yaml

class HoneyCast():
    """HoneyCast main collection"""

    def __init__(self, config_filename):
        with open(config_filename, "r") as config_filehandle:
            self._config = yaml.load(config_filehandle.read())

        self._logger = logging.getLogger("HoneyCast")

        net_config = self._config.get("net", {})

        self._httpd = Process(target=httpd.run, kwargs={
            "port": net_config.get("http_port", 8008),
            "host": "0.0.0.0",
        })

        self._message_channel = MessageChannel("127.0.0.1", 8009)

        discovery_address = net_config.get("discovery_address", "127.0.0.1")
        discovery_port = net_config.get("discovery_port", 0)
        device_config = self._config.get("device", {})

        self._discovery = Discovery(discovery_address, discovery_port, {
            "md": device_config.get("model_name", "Model Name"),
            "id": device_config.get("uuid", random_uuid()),
            "fn": device_config.get("device_name", "Device Name"),
        })

    def start_honeypot_service(self):
        self._httpd.start()
        self._message_channel.start()
        self._discovery.start()
        self._logger.info("Opening socket")

        self._logger.info("Started a fake cast device")

    def stop_honeypot_service(self):
        self._discovery.stop()
        self._message_channel.stop()
        self._httpd.terminate()
        self._httpd.join()


if __name__ == "__main__":
    honeycast = HoneyCast("honeycast.yaml")
    honeycast.start_honeypot_service()
