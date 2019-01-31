# HoneyCast

A honeypot to collect media mistakenly or purposely streamed to Chromecast devices on the internet.

## Why

During the "casthack", a couple of cast-enabled devices on the public internet were attacked to stream videos of a famous YouTube personality. [[1]](http://casthack.thehackergiraffe.com)

This project aims to work with [pychromecast](https://github.com/balloob/pychromecast), a Python implementation of the Chromecast client API. So anyone scanning the internet and connecting to this honeypot shall think this is an actual device and do their shenanigans there.

## Usage

The [Makefile](Makefile) provides a few helpful scripts, such as setting up a virtual environment for development. Once everything's setup, you can use a few command line flags to disable certain services from honeycast:

```bash
(venv) $ ./app.py --help
Usage: app.py [options]

Options:
  -h, --help     show this help message and exit
  --no-web       Don't start eureka webserver
  --no-zeroconf  Don't advertise using zeroconf
  --no-cast      Don't run a cast server
```

Honeycast ships with a Dockerfile, which generates very plain, self-signed X509 certificates during build. You can specify your own certificates in the [config](honeycast.yaml).

## License

honeycast is released under the [MIT license](LICENSE).
