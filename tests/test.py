from unittest import TestCase

from . import ServerTest
from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestWords(ServerTest):

    def testWordWithoutParent(self):
        word_without_parent = {
            'context': [
                'A systray application to quickly change the JACK-DBus configuration from QjackCtl presets.',
            ],
            'context_title': [
                'SpotlightKid/jack-select: A systray application to quickly change the JACK-DBus configuration from QjackCtl presets.',
            ],
            'context_url': ['https://github.com/SpotlightKid/jack-select'],
            'port': ['1001'],
            'tword': ['быстро'],
            'word': ['quickly'],
        },
        response = self.request(word_without_parent)
        print(response)
