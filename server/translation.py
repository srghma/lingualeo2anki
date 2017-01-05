import urllib
import requests

from .config import config
from .utils import debug, dig, download

gettranslates_url = "https://api.lingualeo.com/gettranslates"


class Translation:

    """ Wrapper for lingualeo translation responses """

    @classmethod
    def request(cls, word, include_extra=True):
        debug("Requesting translation for word {}", str(word))
        data = {
            'word': word,
            'include_media':  1 if include_extra else 0,
            'add_word_forms': 1 if include_extra else 0
        }

        response = requests.post(gettranslates_url, data).json()
        debug("Got responce: \n{}", response)
        return cls(word, response)

    def __init__(self, word, body):
        self.word = word
        self.body = body

    def orig_form(self):
        orig_form = dig('word_forms', 0, 'word')
        if self.word != orig_form:
            return orig_form

    def download_media(self, field):
        media_url = dig(self.body, field)
        if not media_url:
            return
        media_name = media_url.split('/')[-1]
        path = download(media_url, media_name, config.media_dir_path)
        if path:
            return media_name

    def download_picture(self):
        return self.download_media('pic_url')

    def download_sound(self):
        return self.download_media('sound_url')

    def twords(self):
        return self.download_media('sound_url')
