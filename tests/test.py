from unittest import TestCase

from . import ServerTest
from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestWords(ServerTest):

    def testInvalidRequest(self):
        invalid_data = {
            'some': 'data',
        }
        response = self.request(invalid_data).json()
        self.assertEqual(response, {'message': 'Must have required fields: word'})

    def testWordWithoutParent(self):
        data_without_parent = {
            'word': 'quickly',
        }
        response = self.request(data_without_parent).json()
        self.assertEqual(response, {})
        self.assertEqual(self.read_csv(), "data")
