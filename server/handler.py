from http.server import SimpleHTTPRequestHandler
import urllib
import json

from .utils import debug
from .lingualeo import Translation
from .errors import InvalidInterceptionError


class Handler(SimpleHTTPRequestHandler):

    # core
    def do_POST(self):
        try:
            debug("Handler: have some data intercepted")
            interception = self.get_interception()

            print(interception["word"])
        except InvalidInterceptionError as err:
            self.send_json(422, {"message": err.message})
            raise

    # helpers
    def get_interception(self):
        try:
            body_lenght = int(self.headers['Content-Length'])
            rawbody = self.rfile.read(body_lenght).decode("utf-8")
            body = urllib.parse.parse_qs(rawbody)

            def get_from_body(key, required=False):
                if required:
                    return body[key][0]
                else:
                    return body.get(key, [None])[0]

            return {
                'word':    get_from_body('word', required=True),
                'context': get_from_body('context'),
            }
        except KeyError as err:
            message = "Must have required fields: %s" % err.args
            raise InvalidInterceptionError(message, rawbody) from err

    def send_json(self, code, data):
        string = json.dumps(data)
        encoded = string.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(encoded)

    # every time server send responce - server logged it
    # let's silent him
    def log_message(self, format, *args):
        return
