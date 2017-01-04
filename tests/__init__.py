from unittest import TestCase
from os import path, makedirs
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import requests
import json
import time

from server.config import config

test_dir_path = path.dirname(__file__)
root_dir_path = path.dirname(test_dir_path)
log_dir_path  = path.join(test_dir_path, 'logs')

if not path.exists(log_dir_path):
    makedirs(log_dir_path)


class ServerTest(TestCase):

    def setUp(self):
        current_test_name = self.id().split('.')[-1]

        debug_name = current_test_name + '.log'
        debug_path = path.join(log_dir_path, debug_name)
        self.debug_file = open(debug_path, 'w')

        csv_name = current_test_name + '.csv'
        self.csv_path = path.join(log_dir_path, csv_name)

        cmd = [
            'python', '-m', 'server',
            '-f', self.csv_path,
            '--debug'
        ]

        self.server = Popen(cmd,
                            universal_newlines=True,
                            cwd=root_dir_path,
                            # start_new_session=True,
                            # shell=True, # XXX: dont use - no output
                            stdout=self.debug_file,
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
            self.debug_file.close()

    def request(self, data):
        server_url = 'http://localhost:%s' % config.port
        encoded = json.dumps(data)
        return requests.post(server_url, encoded)

    def read_csv(self):
        with open(self.csv_path, 'r') as csv:
            return csv.read()
