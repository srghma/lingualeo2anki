from http.server import SimpleHTTPRequestHandler
import urllib

from .utils import debug
from .lingualeo import Translation


class Handler(SimpleHTTPRequestHandler):

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
            debug("Wrong data intercepted (must have word): " + str(body))
            return None

    def do_POST(self):
        debug("Handler: have some data intercepted")
        interception = self.get_interception()

        if not interception:
            return

        print(interception["word"])
