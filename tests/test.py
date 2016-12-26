import os
from os import path
import inspect
from unittest import TestCase

from server.config import config


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))

