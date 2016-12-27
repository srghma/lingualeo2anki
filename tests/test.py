from os import path, system
from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, call

from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent

test_dir_path     = path.dirname(__file__)
root_dir_path     = path.dirname(test_dir_path)
debug_path        = path.join(test_dir_path, "debug.log")

# recreate debug.log
open(debug_path, 'w').close()


class TestAll(TestCase):

    def test_config(self):
        self.assertEqual(config.server_address, ('127.0.0.1', 3100))


class TestHandler(TestCase):

    def setUp(self):
        cmd = [
            'python', '-m', 'server',
            '-f', path.join(test_dir_path, 'anki.csv'),
            '--debug'
        ]
        self.debug_file = open(debug_path, 'a')
        self.server = Popen(cmd, universal_newlines=True, cwd=root_dir_path,
                            stdout=self.debug_file, stderr=STDOUT)

    def tearDown(self):
        try:
            self.server.communicate(timeout=2)
        except TimeoutExpired:
            self.server.kill()
            # self.server.communicate()
            # kill_listener = "lsof -i :3100 | awk '{ print $2 }' | tail -n +2 | xargs kill"
            # system(kill_listener)
        finally:
            self.debug_file.close()

    def testWordWithoutParent(self):
        print("")
        # pass
