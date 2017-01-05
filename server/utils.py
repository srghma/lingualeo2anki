from os import path, makedirs
import pprint
from functools import reduce
import requests

from .config import config
from .errors import DigError


def debug(data, *args):
    if config.debug:
        args = [pprint.pformat(arg) for arg in args]
        print("DEBUG: ", data.format(*args))


def create_file(file_path):

    """create file if it doesn't exist"""

    if not path.isfile(file_path):
        open(file_path, 'a').close()


def create_dir(dir_path):

    """create directory if it doesn't exist"""

    if not path.exists(dir_path):
        makedirs(dir_path)


def dig(dictionary, *keys, default=None, raise_error=False):

    def get_item(end_of_chain, key):
        if end_of_chain == default:
            return default

        try:
            output = end_of_chain[key]
            return output
        except (KeyError, IndexError, TypeError) as err:
            if raise_error:
                raise DigError(dictionary, key) from err
            else:
                return default

    return reduce(get_item, keys, dictionary)


def download(url, file_name, directory, rewrite=False):

    """If file was downloaded successfully - return file_path"""

    file_path = path.join(directory, file_name)
    if not path.isfile(file_path) or rewrite:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
            return file_path
