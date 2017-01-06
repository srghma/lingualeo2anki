from unittest import TestCase
from os import path
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import requests
import urllib
import json
import time

from server.config import config
from server.utils import create_dir, recreate_dir

tests_dir_path = path.dirname(__file__)
root_dir_path = path.dirname(tests_dir_path)
output_dir_path = path.join(tests_dir_path, 'output')

recreate_dir(output_dir_path)


class ServerTest(TestCase):

    def setUp(self):
        test_name = self.id().split('.')[-1]

        test_dir_path = path.join(output_dir_path, test_name)
        create_dir(test_dir_path)

        stdout_path = path.join(test_dir_path, 'stdout.log')
        self.stdout_file = open(stdout_path, 'w')

        self.output_file_path = path.join(test_dir_path, 'anki.txt')

        self.media_dir_path = path.join(test_dir_path, 'media')
        create_dir(self.media_dir_path)

        cmd = [
            'python', '-m', 'server',
            '-f', self.output_file_path,
            '-m', self.media_dir_path,
            '--debug'
        ]

        self.server = Popen(cmd,
                            universal_newlines=True,
                            cwd=root_dir_path,
                            # start_new_session=True,
                            # shell=True, # XXX: dont use - no output
                            stdout=self.stdout_file,
                            stderr=STDOUT)
        # wait for server to start
        time.sleep(1)

    def tearDown(self):
        try:
            self.server.communicate(timeout=2)
        except TimeoutExpired:
            self.server.terminate()
            self.server.communicate()
        finally:
            self.stdout_file.close()
            # wait for server to stop
            time.sleep(1)

    def request(self, data):
        server_url = 'http://localhost:%s' % config.port
        encoded = urllib.parse.urlencode(data)
        try:
            return requests.post(server_url, encoded)
        except requests.exceptions.ConnectionError:
            return None

    def read_csv(self):
        if not path.isfile(self.output_file_path):
            return None

        with open(self.output_file_path, 'r') as csv:
            return csv.read()
