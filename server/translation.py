import urllib
import requests
from memoized_property import memoized_property

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
        orig_form = dig(self.body, 'word_forms', 0, 'word')
        debug("Orig form: ", str(orig_form))
        if self.word != orig_form:
            return orig_form

    def download_picture(self):
        return self._download_media('pic_url')

    def download_sound(self):
        return self._download_media('sound_url')

    @memoized_property
    def translations(self):

        """ sorted and unique """

        sorted_tr = sorted(self.body['translate'], key=lambda t: t['votes'])
        unique = {}
        for translation in sorted_tr:
            value = translation['value']
            if value not in unique:
                unique[value] = translation
        return unique.values()

    def twords(self, preffered_translation=None):

        """ collect values, return string """
        """ if translation was preffered - it will be on top """

        twords = [t['value'] for t in self.translations]

        if preffered_translation:
            index = twords.index(preffered_translation)
            if index and index != 0:
                twords.insert(0, twords.pop(index))
            else:
                twords.insert(0, preffered_translation)

        return ', '.join(twords)

    def transcr(self):
        return dig(self.body, 'transcription')

    def _download_media(self, field):
        media_url = dig(self.body, field)
        if not media_url:
            return
        media_name = media_url.split('/')[-1]
        path = download(media_url, media_name, config.media_dir_path)
        if path:
            return media_name
