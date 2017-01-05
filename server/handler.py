from http.server import SimpleHTTPRequestHandler
import urllib
import json

from .utils import debug, dig, write_asyncly, bold, more_contexts
from .translation import Translation
from .errors import InvalidInterceptionError, DigError
from .config import config


class Handler(SimpleHTTPRequestHandler):

    # core
    def do_POST(self):
        try:
            interception = self.get_interception()
            word = interception["word"]
            context = interception["context"]

            if context: context = bold(context, word)

            translation = Translation.request(word)
            orig_form = translation.orig_form()

            if orig_form:
                word = orig_form
                parent = Translation.request(orig_form)
                twords = parent.twords()
                transcr = parent.transcr()
                pic_name = parent.download_picture()
            else:
                twords = translation.twords(preffered_translation=interception["tword"])
                transcr = translation.transcr()
                pic_name = translation.download_picture()

            extra_contexts_count = 2 if context else 3
            extra_contexts = more_contexts(word, extra_contexts_count)
            extra_contexts = [bold(context, word) for context in extra_contexts]
            if context: extra_contexts.insert(0, context)
            context = "<br><br>".join(extra_contexts)

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
            return {
                'word': get_from_body('word', required=True),
                'context': get_from_body('context'),
                'tword': get_from_body('tword'),  # translation, that user have picked
            }
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
        args = [' ' if arg is None else arg for arg in args]
        output = config.join_symbol.join(args)
        output += '\n'
        write_asyncly(config.csv_path, output)

    # every time server send responce - server logged it
    # let's silent him
    def log_message(self, format, *args):
        return
