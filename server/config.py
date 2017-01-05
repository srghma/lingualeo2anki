from os import path
from collections import MutableMapping

defaults = {
    "csv_path": path.join(path.expanduser("~"), 'anki.csv'),
    "media_dir_path": path.join(
        path.expanduser("~"), 'Documents', 'Anki', 'User 1', 'collection.media'
    ),

    "join_symbol": '|',
    "address": '127.0.0.1',
    "port": 3100,

    "debug": False,
}


class ConfigHolder(object):
    def __init__(self, init=defaults):
        self.__dict__.update(init)

    def update(self, other):
        self.csv_path       = other.csv_path
        self.media_dir_path = other.media_dir_path
        self.join_symbol    = other.join_symbol
        self.port           = other.port
        self.debug          = other.debug

    @property
    def server_address(self):
        return (self.address, self.port)

    @property
    def csv_path(self):
        return self.__dict__["csv_path"]

    @csv_path.setter
    def csv_path(self, value):
        self.__dict__["csv_path"] = path.abspath(value)

    @property
    def media_dir_path(self):
        return self.__dict__["media_dir_path"]

    @media_dir_path.setter
    def media_dir_path(self, value):
        self.__dict__["media_dir_path"] = path.abspath(value)


config = ConfigHolder()
