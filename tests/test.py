from os import path, getcwd, kill
import inspect
from unittest import TestCase
from subprocess import Popen, PIPE

from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent

test_dir_path     = path.dirname(__file__)
debug_path        = path.join(test_dir_path, "debug.log")
start_server_path = path.join(path.dirname(test_dir_path), 'start_server.sh')

# recriate debug.log
open(debug_path, 'w').close()


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestHandler(TestCase):

    def setUp(self):
        cmd = [
            'python -m server',
            '-f', path.join(test_dir_path, 'anki.csv'),
            '--debug'
        ]
        self.debug_file = open(debug_path, 'a')
        self.server = Popen(cmd, shell=False, universal_newlines=True,
                            stdout=self.debug_file, stderr=PIPE)

    def tearDown(self):
        (_, stderr) = self.server.communicate()
        print(stderr)
        print(self.server.pid)
        self.server.terminate()
        self.debug_file.close()
        try:
            kill(self.server.pid, 0)
            self.server.kill()
            print("Forced kill")
        except OSError:
            print("Terminated gracefully")

    def testWordWithoutParent(self):
        print("test")
        # pass
