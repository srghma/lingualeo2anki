from os import path, system
from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, call

from server.config import config
from .testdata import testdata_without_parent, testdata_with_parent

test_dir_path = path.dirname(__file__)
root_dir_path = path.dirname(test_dir_path)


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
        self.server = Popen(cmd, universal_newlines=True, cwd=root_dir_path,
                            stdout=PIPE, stderr=PIPE)

    def tearDown(self):
        try:
            outs, errs = self.server.communicate(timeout=2)
            print(outs, errs)
        except TimeoutExpired:
            print("kill")
            self.server.kill()
            outs, errs = self.server.communicate()
            print(outs, errs)
            # system("lsof -i :3100 | awk '{ print $2 }' | tail -n +2 | xargs kill")

    def testWordWithoutParent(self):
        print("")
        # pass
