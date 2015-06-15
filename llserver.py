#!/usr/bin/env python
import sys
import urllib
import requests
import simplejson as json
from os import path
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pprintpp import pprint as pp

filePath = path.join(
    path.expanduser('~'), 'Documents', 'LINGUALEO', 'test.csv')
picDirPath = path.join(
    path.expanduser('~'), 'Documents', 'Anki', 'User 1', 'collection.media')
joinSymbol = '|'

isSupportHtml = True
isSavePictures = True


class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):
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
        if (isSupportHtml):
            data['context'] = data['context'].replace(
                data['orig_word'], "<b>" + data['orig_word'] + "</b>")

        orig_transl = self.get_word_info(interception['word'])
        data['sound_url'] = orig_transl.get('sound_url', None)

        try:
            transl = self.get_word_info(orig_transl['word_forms'][0]['word'])
            pic_url = transl.get('pic_url', None)
            pic_name = pic_url.split('/')[-1] if pic_url else ''
            if (isSavePictures and pic_name):
                self.dowload_pic(pic_url, pic_name)

            data['pic_name'] = pic_name
            data['word'] = transl['word_forms'][0]['word']
            data['type'] = transl['word_forms'][0]['type']
            data['translations'] = ', '.join(
                [t['value'] for t in transl['translate']])
            data['transcription'] = transl['transcription']
        except IndexError:
            data['word'] = data['orig_word']
            data['translations'] = ''

        pp(data)
        line = data['word'] + joinSymbol + \
            data['translations'] + joinSymbol + \
            data['transcription'] + joinSymbol + \
            data['pic_name'] + joinSymbol + \
            data['context'] + "\n"
        with open(filePath, "a") as text_file:
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
    from optparse import OptionParser
    op = OptionParser()
    op.add_option("-p", default=3000, type="int", dest="port",
                  help="port #")
    op.add_option("-f", "--file", dest="filePath", default=filePath,
                  help="write word data to FILE", metavar="FILE")
    op.add_option("-d", "--dir", dest="picDirPath", default=picDirPath,
                  help="save images to DIRECTORY", metavar="FILE")
    op.add_option("-j", "--join", dest="joinSymbol", default=joinSymbol,
                  help="a symbol which connects up words")
    op.add_option("--nohtml", action="store_false", dest="isSupportHtml", default=isSupportHtml,
                  help="don`t mark words in context")
    op.add_option("--nopic", action="store_false", dest="isSavePictures", default=isSavePictures,
                  help="don`t save pictures in folder (Anki folder in default)")
    opts, args = op.parse_args(sys.argv)

    server_address = ('127.0.0.1', opts.port)
    filePath = opts.filePath
    picDirPath = opts.picDirPath
    joinSymbol = opts.joinSymbol
    isSupportHtml = opts.isSupportHtml
    isSavePictures = opts.isSavePictures

    print(opts)

    if (not path.isfile(filePath)):
        open(filePath, 'a').close() #create if doesn't exist
    if (not path.isdir(picDirPath)):
        sys.exit("Wrong path to save images")

    httpd = HTTPServer(server_address, Handler)
    print('http server is running...listening on port %s' % server_address[1])

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        sys.exit(1)
    finally:
        httpd.server_close()
