import urllib
import requests

from .utils import debug

gettranslates_url = "https://api.lingualeo.com/gettranslates"


class Translation:

    """ Wrapper for lingualeo translation responses """

    @classmethod
    def request(cls, word, include_extra=True):
        data = {
            'word': word,
            'include_media':  1 if include_extra else 0,
            'add_word_forms': 1 if include_extra else 0
        }

        response = requests.post(gettranslates_url, data).json()
        debug("Request translation, get responce: {}", response)

    def __init__(self, rawdata):
        self.rawdata = rawdata
