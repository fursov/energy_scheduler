#!/usr/bin/env python

import yaml

CONFIG_FILE_NAME = 'config.yaml'


class SchedulerConfig():
    def __init__(self):
        self._read_config()

    def _read_config(self):
        with open(CONFIG_FILE_NAME, 'r') as stream:
            self.config = yaml.safe_load(stream)

    def save_config(self):
        with open(CONFIG_FILE_NAME, 'w') as stream:
            yaml.dump(self.config, stream)

    def add_device(device):
        pass
