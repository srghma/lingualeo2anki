from os import path, makedirs
from shutil import rmtree
import pprint
from functools import reduce
import requests
from threading import Thread
from bs4 import BeautifulSoup

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


def recreate_dir(dir_path):
    if path.exists(dir_path):
        rmtree(dir_path)
    makedirs(dir_path)


def dig(dictionary, *keys, default=None, raise_error=False):

    end_of_chain = dictionary
    try:
        for key in keys:
            end_of_chain = end_of_chain[key]
    except (KeyError, IndexError) as err:
        if raise_error:
            raise DigError(dictionary, keys) from err
        else:
            return default

    return end_of_chain


def download(url, file_name, directory):

    """If file was downloaded successfully - return file_path"""

    file_path = path.join(directory, file_name)

    if path.isfile(file_path):
        return file_path

    r = requests.get(url, stream=True)

    if r.status_code != 200:
        return None

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)
    return file_path


def write_asyncly(path, data):
    def write(path, data):
        with open(path, 'a') as f:
            return f.write(data)

    Thread(target=write, args=(path, data)).start()


def request_usage_examples(word, amount):
    url = "http://dictionary.reference.com/browse/{}".format(word)
    try:
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        examples = soup.find_all(class_="partner-example-text", limit=amount)
        examples = [example.getText() for example in examples]

        return examples
    except requests.exceptions.Timeout:
        return None


def bold(data, word):
    def bold_string(string, word):
        return string.replace(word, "<b>" + word + "</b>")

    if isinstance(data, str):
        return bold_string(data, word)

    return [bold_string(item, word) for item in data]


def clean(data, prohibited_chars=None):
    if prohibited_chars is None:
        prohibited_chars = ' \n\r'  # trailing whitespace and newlines
        prohibited_chars += config.join_symbol

    def clean_string(string, prohibited_chars):
        return string.strip(prohibited_chars)

    if isinstance(data, str):
        return clean_string(data, prohibited_chars)

    return [clean_string(item, prohibited_chars) for item in data]
