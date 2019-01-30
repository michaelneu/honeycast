import logging
logging.basicConfig(level=logging.DEBUG)

import pychromecast
from honeycast import HoneyCast

honeycast = HoneyCast("honeycast.yaml")

honeycast.start_honeypot_service()

chromecasts = pychromecast.get_chromecasts()

for chromecast in chromecasts:
    print(chromecast.device.friendly_name)

# honeycast.stop_honeypot_service()
