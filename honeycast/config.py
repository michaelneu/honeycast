import os
import yaml

class ConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Config:
    @staticmethod
    def from_file(filename):
        with open(filename, "r") as file_handle:
            raw_config = yaml.load(file_handle)

        return Config(raw_config)

    def __init__(self, config):
        self._config = config

    def get(self, path, default=None):
        config = self._config
        parts = path.split(".")

        for part in parts:
            print("searching", part)
            config = config.get(part, None)

            if config is None:
                raise ConfigException("invalid path: can't find '%s'" % path)

        if isinstance(config, dict):
            return Config(config)

        return config or default

config = Config.from_file("honeycast.yaml")
