from os import path
from collections import MutableMapping

defaults = {
    "write_to_path":   path.join(path.expanduser("~"), 'anki.csv'),
    "images_dir_path": path.join(
        path.expanduser("~"), 'Documents', 'Anki', 'User 1', 'collection.media'
    ),

    "join_symbol":     '|',
    "address":         '127.0.0.1',
    "port":            3100,

    "debug":           False,
}


class ConfigHolder(object):
    def __init__(self, init=defaults):
        self.__dict__.update(init)

    @property
    def server_address(self):
        return (self.address, self.port)

    @property
    def write_to_path(self):
        return self.__dict__["write_to_path"]

    @write_to_path.setter
    def write_to_path(self, value):
        self.__dict__["write_to_path"] = path.abspath(value)

    @property
    def images_dir_path(self):
        return self.__dict__["images_dir_path"]

    @images_dir_path.setter
    def images_dir_path(self, value):
        self.__dict__["images_dir_path"] = path.abspath(value)


config = ConfigHolder()
