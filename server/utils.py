from .config import config
from os import path


def debug(str, *args):
    if config.debug:
        print("DEBUG: ", str % args)


def create_file(file_path):

    """create file if it doesn't exist"""

    if not path.isfile(file_path):
        open(file_path, 'a').close()
