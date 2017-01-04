from os import path
import pprint

from .config import config


def debug(data, *args):
    if config.debug:
        args = [pprint.pformat(arg) for arg in args]
        print("DEBUG: ", data.format(args))


def create_file(file_path):

    """create file if it doesn't exist"""

    if not path.isfile(file_path):
        open(file_path, 'a').close()
