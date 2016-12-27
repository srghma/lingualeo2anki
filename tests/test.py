from os import path, getcwd, kill
import inspect
import sys
from unittest import TestCase
from subprocess import Popen, PIPE, TimeoutExpired
from server.config import config

from .testdata import testdata_without_parent, testdata_with_parent

test_dir_path     = path.dirname(__file__)
root_dir_path     = path.dirname(test_dir_path)
start_server_path = path.join(root_dir_path, "start_server.sh")


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestHandler(TestCase):

    def setUp(self):
        cmd = [
            start_server_path,
            '-f', path.join(test_dir_path, 'anki.csv'),
            '--debug'
        ]
        self.server = Popen(cmd, shell=False, universal_newlines=True,
                            stdout=PIPE, stderr=PIPE)

    def tearDown(self):
        # self.debug_file.close()
        try:
            stdout, stderr = self.server.communicate(timeout=2)
        except TimeoutExpired:
            print("here")
            self.server.kill()
            stdout, stderr = self.server.communicate()
        finally:
            print(stdout, stderr)

    def testWordWithoutParent(self):
        print("")
        # pass
