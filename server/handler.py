from http.server import SimpleHTTPRequestHandler
import urllib
import json
from collections import OrderedDict
from colorama import Fore, Back, Style
from memoized_property import memoized_property

from .utils import debug, dig, write_asyncly, bold, request_usage_examples, clean
from .translation import Translation
from .errors import InvalidInterceptionError, DigError
from .config import config


class Handler(SimpleHTTPRequestHandler):

    # core
    def do_POST(self):
        try:
            translation = Translation.request(self.interception["word"])
            orig_form = translation.orig_form()

            if not orig_form:
                word = self.interception["word"]
                twords = translation.twords(preffered_translation=self.interception["tword"])
                transcr = translation.transcr()
                pic_name = translation.download_picture()
            else:
                word = orig_form
                parent = Translation.request(orig_form)
                twords = parent.twords(preffered_translation=self.interception["tword"])
                transcr = parent.transcr()
                pic_name = parent.download_picture()

            usage_examples = self.make_usage_examples(
                amount=3,
                word=word,
                include_context=True)

            output = OrderedDict()
            output["word"]     = word
            output["twords"]   = twords
            output["transcr"]  = transcr
            output["pic_name"] = pic_name
            output["usage_examples"] = usage_examples

            self.send_json(200, translation.body)
            self.write_to_csv(output)
            self.print(output)
        except InvalidInterceptionError as err:
            debug("InvalidInterceptionError occured: {}", err.message)
            self.send_json(422, {"message": err.message})

    def make_usage_examples(self, amount, word, include_context):
        context = self.interception['context'] if include_context else None
        request_amount = amount

        if context:
            request_amount -= 1
            context = clean(context)
            context = bold(context, self.interception["word"])

        examples = request_usage_examples(word, request_amount)
        examples = clean(examples)
        examples = bold(examples, word)

        if context:
            examples.insert(0, context)

        return "<br><br>".join(examples)

    # helpers
    @memoized_property
    def interception(self):
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
            message = "Must have required field: {}".format(err.path[0])
            raise InvalidInterceptionError(message) from err

    def send_json(self, code, data):
        string = json.dumps(data)
        encoded = string.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(encoded)

    def write_to_csv(self, dictionary):
        values = dictionary.values()
        values = [' ' if value is None else value for value in values]

        output = config.join_symbol.join(values)
        output += '\n'
        write_asyncly(config.csv_path, output)

    def print(self, dictionary):
        if config.silent:
            return

        for key, value in dictionary.items():
            buffer = Fore.RED + key + ':\t'
            if not value:
                buffer += Style.DIM
            buffer += Fore.GREEN + str(value)
            buffer += Style.RESET_ALL
            print(buffer)
        print('\n')

    # every time server send responce - server logged it
    # let's silent him
    def log_message(self, format, *args):
        return
