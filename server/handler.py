from http.server import SimpleHTTPRequestHandler
import urllib
import json

from .utils import debug, dig
from .translation import Translation
from .errors import InvalidInterceptionError, DigError


class Handler(SimpleHTTPRequestHandler):

    # core
    def do_POST(self):
        try:
            word, context = self.get_interception()

            translation = Translation.request(word)
            orig_form = translation.orig_form()
            debug("Orig form: ", str(orig_form))

            if orig_form:
                parent = Translation.request(orig_form)
            else:
                twords = translation.twords
                transcr = translation.transcr
                pic_url = translation.pic_url

            self.send_json(200, translation.body)
            self.write_to_csv(word,
                              twords,
                              transcr,
                              pic_name,
                              context)
        except InvalidInterceptionError as err:
            self.send_json(422, {"message": err.message})

    # helpers
    def get_interception(self):
        body_lenght = int(self.headers['Content-Length'])
        rawbody = self.rfile.read(body_lenght).decode("utf-8")

        debug("Intercepted: {}", rawbody)

        body = urllib.parse.parse_qs(rawbody)

        def get_from_body(key, required=False):
            return dig(body, key, 0, raise_error=required)

        try:
            return (
                get_from_body('word', required=True),
                get_from_body('context')
            )
        except DigError as err:
            message = "Must have required field: {}".format(err.key)
            raise InvalidInterceptionError(message) from err

    def send_json(self, code, data):
        string = json.dumps(data)
        encoded = string.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(encoded)

    def write_to_csv(self, *args):
        output = config.join_symbol.join(*args)
        output += '\n'
        with open(self.csv_path, 'a') as csv:
            return csv.write(output)

    # every time server send responce - server logged it
    # let's silent him
    def log_message(self, format, *args):
        return
