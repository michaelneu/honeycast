#!/usr/bin/env python3

from honeycast.cast import CastServer, CastException
from honeycast.config import config
from honeycast.discovery import Discovery
from honeycast.web import httpd
from multiprocessing import Process
from optparse import OptionParser
from uuid import uuid4

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--no-web", action="store_false", dest="web", default=True, help="Don't start eureka webserver")
    parser.add_option("--no-zeroconf", action="store_false", dest="zeroconf", default=True, help="Don't advertise using zeroconf")
    parser.add_option("--no-cast", action="store_false", dest="cast", default=True, help="Don't run a cast server")
    options, _ = parser.parse_args()

    processes = []

    if options.web:
        http_process = Process(target=httpd.run, kwargs={
            "port": config.get("net.http.port", 8008),
            "host": config.get("net.http.host", "0.0.0.0"),
        })
        processes.append(http_process)

    if options.zeroconf:
        zeroconf = Discovery(
            zeroconf_name=config.get("net.discovery.zeroconf_name", "cast"),
            address=config.get("net.discovery.address", "127.0.0.1"),
            port=config.get("net.discovery.port", 0),
            model_name=config.get("device.model_name", "Cast"),
            uuid=config.get("device.uuid", uuid4()),
        )
        zeroconf_process = Process(target=zeroconf.run)
        processes.append(zeroconf_process)

    if options.cast:
        server = CastServer(
            port=config.get("net.cast.port", 8009),
            key_path=config.get("net.cast.key", "key.pem"),
            cert_path=config.get("net.cast.certificate", "certificate.pem"),
        )
        server_process = Process(target=server.run)
        processes.append(server_process)

    for process in processes:
        process.start()

