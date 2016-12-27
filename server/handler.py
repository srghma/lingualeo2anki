from http.server import SimpleHTTPRequestHandler
import urllib

from .lingualeo import Lingualeo


class Handler(SimpleHTTPRequestHandler):

    allow_reuse_address = True

    def get_requested_word(self):
        body_lenght = int(self.headers['Content-Length'])
        rawbody = self.rfile.read(body_lenght).decode("utf-8")
        body = urllib.parse.parse_qs(rawbody)
        return body['word'][0]

    def do_POST(self):
        print(get_requested_word())
