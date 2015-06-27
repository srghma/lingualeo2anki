#!/usr/bin/env python
import sys
import urllib
import requests
import simplejson as json
from os import path
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pprintpp import pprint as pp

FILE_PATH = path.join(path.expanduser('~'), 'anki.csv')
IMAGE_DIR_PATH = path.join(path.expanduser('~'), 'Documents', 'Anki', 'User 1', 'collection.media')
JOIN_SYMBOL = '|'

SUPPORT_HTML = True
SAVE_PICTURES = True

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_cap()
        data = {
            "orig_word": None,
            "word": None,
            "type": None,
            "translations": None,
            "transcription": None,
            "context": None,
            "pic_name": None,
            "sound_url": None #for future
        }

        interception = self.get_interception()
        self.send_cap()
        data['orig_word'] = interception['word'][0]
        data['context'] = interception['context_title'][0]
        if (SUPPORT_HTML):
            data['context'] = data['context'].replace(
                data['request_word'], "<b>" + data['request_word'] + "</b>")
        
        orig_transl = get_word_info(request_word)
        data['sound_url'] = orig_transl.get('sound_url', None)
        
        try:
            transl = get_word_info(orig_transl['word_forms'][0]['word'])
            pic_url = transl.get('pic_url', None)
            pic_name = pic_url.split('/')[-1] if pic_url else ''
            if (SAVE_PICTURES and pic_name):
                dowload_pic(pic_url, pic_name)
        
            data['pic_name'] = pic_name
            data['word'] = transl['word_forms'][0]['word']
            data['type'] = transl['word_forms'][0]['type']
            data['translations'] = ', '.join(
                [t['value'] for t in transl['translate']])
            data['transcription'] = transl['transcription']
        except IndexError:
            data['word'] = data['request_word']
        
        pp(data)
        line = data['word'] + JOIN_SYMBOL + \
            data['translations'] + JOIN_SYMBOL + \
            data['transcription'] + JOIN_SYMBOL + \
            data['pic_name'] + JOIN_SYMBOL + \
            data['context'] + "\n"
        with open(FILE_PATH, "a") as text_file:
            text_file.write(line)

    def get_interception(self):
        rawbody = self.rfile.read(
            int(self.headers['Content-Length'])).decode("utf-8")
        return urllib.parse.parse_qs(rawbody)

    def send_cap(self):
        # TODO
        # prevent error message in extention (not work)
        pass
        # self.send_response(200)

    def get_word_info(self, word, host="https://api.lingualeo.com/gettranslates", include_media=1, add_word_forms=1):
        data = {
            'word': word,
            'include_media': include_media,
            'add_word_forms': add_word_forms
        }
        return requests.post(host, data).json()

    def dowload_pic(self, pic_url, pic_name):
        dir_path = picDirPath
        if (not pic_url):
            raise ValueError("pic_url is empty")
        pic_path = path.join(dir_path, pic_name)
        if (path.isfile(pic_path)):
            # there no need to rewrite the file
            return
        r = requests.get(pic_url, stream=True)
        if r.status_code == 200:
            with open(pic_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file_path", default=FILE_PATH,
                      help="write word data to FILE", metavar="FILE")
    parser.add_argument("-i", "--images", dest="image_dir_path", default=IMAGE_DIR_PATH,
                      help="save images to DIRECTORY", metavar="FILE")
    parser.add_argument("-j", "--join", dest="join_symbol", default=JOIN_SYMBOL,
                      help="a symbol which connects up words")
    parser.add_argument("--nohtml", action="store_false", dest="support_html", default=SUPPORT_HTML,
                      help="don`t mark words in context")
    parser.add_argument("--nopic", action="store_false", dest="save_pictures", default=SAVE_PICTURES,
                      help="don't save pictures in folder (Anki folder in default)")
    opts = parser.parse_args()

    server_address = ('127.0.0.1', 3000)
    FILE_PATH = path.abspath(opts.file_path)
    IMAGE_DIR_PATH = path.abspath(opts.image_dir_path)
    JOIN_SYMBOL = opts.join_symbol
    SUPPORT_HTML = opts.support_html
    SAVE_PICTURES = opts.save_pictures

    if (not path.isfile(FILE_PATH)):
        open(FILE_PATH, 'a').close()  # create if doesn't exist
    if (not path.isdir(IMAGE_DIR_PATH)):
        sys.exit("%s is wrong path to save images" % IMAGE_DIR_PATH)

    print("Word data will be writen to %s" % FILE_PATH)
    print("Images will be saved to %s" % IMAGE_DIR_PATH)

    httpd = HTTPServer(server_address, Handler)
    print('http server is running...listening on port %s' % server_address[1])

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        httpd.server_close()
