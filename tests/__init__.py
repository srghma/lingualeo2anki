from unittest import TestCase
from os import path, system
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, call
import requests
import json

from server.config import config

test_dir_path = path.dirname(__file__)
root_dir_path = path.dirname(test_dir_path)
write_to_path = path.join(test_dir_path, 'anki.csv')


class ServerTest(TestCase):

    def setUp(self):
        cmd = [
            'python', '-m', 'server',
            '-f', write_to_path,
            '--debug'
        ]

        debug_file_name = self.id().split('.')[-1] + '.log'
        debug_path = path.join(test_dir_path, debug_file_name)
        self.debug_file = open(debug_path, 'w')

        self.server = Popen(cmd,
                            universal_newlines=True,
                            cwd=root_dir_path,
                            # start_new_session=True,
                            # shell=True, # XXX: dont use - no output
                            stdout=self.debug_file,
                            stderr=PIPE)

    def tearDown(self):
        try:
            _, stderr = self.server.communicate(timeout=2)
            print(stderr)
        except TimeoutExpired:
            self.server.terminate()
            _, stderr = self.server.communicate()
            print(stderr)
        finally:
            self.debug_file.close()

    def request(self, data):
        server_url = 'http://localhost:' + str(config.port)
        encoded = json.dumps(data)
        return requests.post(server_url, encoded).json()
