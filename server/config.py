from os import path
from collections import MutableMapping

defaults = {
    "output_file_path": path.join(path.expanduser("~"), 'anki.txt'),
    "media_dir_path": path.join(
        path.expanduser("~"), 'Documents', 'Anki', 'User 1', 'collection.media'
    ),

    "join_symbol": '\t',
    "address": '127.0.0.1',
    "port": 3100,

    "debug": False,
    "silent": False,
}


class ConfigHolder(object):
    def __init__(self, init=defaults):
        self.__dict__.update(init)

    def update(self, other):
        self.output_file_path = other.output_file_path
        self.media_dir_path   = other.media_dir_path
        self.join_symbol      = other.join_symbol
        self.port             = other.port
        self.debug            = other.debug
        self.silent           = other.silent

    @property
    def server_address(self):
        return (self.address, self.port)

    @property
    def output_file_path(self):
        return self.__dict__["output_file_path"]

    @output_file_path.setter
    def output_file_path(self, value):
        self.__dict__["output_file_path"] = path.abspath(value)

    @property
    def media_dir_path(self):
        return self.__dict__["media_dir_path"]

    @media_dir_path.setter
    def media_dir_path(self, value):
        self.__dict__["media_dir_path"] = path.abspath(value)


config = ConfigHolder()
