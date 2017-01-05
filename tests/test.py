from unittest import TestCase

from . import ServerTest
from server.config import config
from server.utils import dig
from server.errors import DigError
from .testdata import testdata_without_parent, testdata_with_parent


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))

    def test_dig(self):
        dictionary = {
            'a': {
                'b': 'tuna',
                'c': 'fish',
                'list': [
                    {'x': 'peanut butter'},
                    {'y': 'jelly'},
                ]
            },
            'b': {}
        }

        self.assertEqual(
            dig(dictionary, 'a', 'b'),
            'tuna'
        )

        self.assertEqual(
            dig(dictionary, 'a', 'list', 0),
            {'x': 'peanut butter'}
        )

        self.assertEqual(
            dig(dictionary, 'a', 'list', 3, default="some"),
            "some"
        )

        with self.assertRaises(DigError):
            dig(dictionary, 'a', 'list', 3, raise_error=True)


class TestWords(ServerTest):

    def testInvalidRequest(self):
        invalid_data = {
            'some': 'data',
        }
        resp = self.request(invalid_data).json()
        self.assertEqual(resp, {'message': 'Must have required field: word'})
        self.assertIsNone(self.read_csv())

    def testWordWithoutParent(self):
        data_without_parent = {
            'word': 'quickly',
        }
        resp = self.request(data_without_parent).json()
        self.assertTrue(resp)
        self.assertTrue(self.read_csv().startswith('quickly|'))

    def testWordWithParent(self):
        data_with_parent = {
            'word': 'issues',
            'context': 'There you can report issues',
            'tword': 'проблемы',
        }
        resp = self.request(data_with_parent).json()
        self.assertTrue(resp)
        self.assertTrue(self.read_csv().startswith('issue|'))
