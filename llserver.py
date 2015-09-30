#!/usr/bin/env python
import requests
import simplejson as json
from os import path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import pprint; from pprintpp import pprint as pp
from PyDictionary import PyDictionary; dictionary=PyDictionary()

DEBUG = True
FILE_PATH = path.join(path.dirname(path.realpath(__file__)), 'anki.csv')
MEDIA_DIR_PATH = '/home/bjorn/Documents/Anki/User 1/collection.media'
JOIN_SYMBOL = '|'

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        from functools import reduce

        intercept = self.get_interception()
        original_form = Helper.get_lingualeo_data(intercept['orig_form']['word'])

        # if word have different orig form - take data from orig_form
        if (intercept['word'] == intercept['orig_form']['word']):
            templ = intercept
        else: templ = original_form

        if intercept['context']:
            context = Helper.context_example(templ['word'], 2)
            context.insert(0, intercept['context'])
        else:
            context = Helper.context_example(templ['word'], 3)
        context = "<br><br>".join(context)

        synonyms = { key: Helper.translate(key) for key in dictionary.synonym(templ['word']) }
        try:
            data = {
                'word':              templ['word'],
                'twords':            ', '.join(templ['twords']),
                'transcr':           templ['transcr'],
                'pic_name':          Helper.dowload(templ['pic_url']),
                # 'sound_name':        Helper.dowload(templ['sound_url']),
                'context':           Helper.distinguish(templ['word'], context ),
                'synonyms':          ', '.join( synonyms.keys() ),
                'synonyms_&_transl': ', '.join([key+'('+value+')' for key, value in synonyms.items()]),
            }

            pp(data)

            line =  data['word'] + JOIN_SYMBOL + \
                    data['twords'] + JOIN_SYMBOL + \
                    data['transcr'] + JOIN_SYMBOL + \
                    data['pic_name'] + JOIN_SYMBOL + \
                    data['context'] + JOIN_SYMBOL + \
                    data['synonyms'] + JOIN_SYMBOL + \
                    data['synonyms_&_transl'] + "\n"
            with open(FILE_PATH, "a", encoding = 'utf-8') as text_file:
                text_file.write(line)

        except Exception as e:
            pp(intercept)
            pp(original_form)
            pp(context)
            pp(synonyms)
            raise e
        print('#'*100)

    def get_interception(self):
        import urllib

        body_lenght = int(self.headers['Content-Length'])
        rawbody = self.rfile.read(body_lenght).decode("utf-8")
        body = urllib.parse.parse_qs(rawbody)
        try:
            word = body['word'][0]
            transl = Helper.get_lingualeo_data(word)
            interception = {
                'word':          word,
                'transcr':       transl['transcr'],
                'twords':        transl['twords'],
            }

            interception['context'] = " ".join(body['context']).replace('\n', '') if body['context'] else ''
            interception['context_title'] = body.get('context_title', [''])[0]
            interception['context_url'] = body.get('context_url', [''])[0]
            interception['orig_form'] = transl.get('orig_form', '')
            interception['pic_url'] = transl.get('pic_url', '')
            interception['sound_url'] = transl.get('sound_url', '')
        except Exception as e:
            pp(body)
            raise e

        Helper.insert_to_top(body['tword'][0], interception['twords'])
        return interception

class Helper:
    @classmethod
    def get_lingualeo_data(self, word, include_extra = True, host="https://api.lingualeo.com/gettranslates"):
        data = {
            'word': word,
            'include_media': 1 if include_extra else 0,
            'add_word_forms': 1 if include_extra else 0
        }
        response = requests.post(host, data).json()

        word_info = {
            'transcr': response['transcription'],
            'twords': [ t['value'] for t in response['translate'] ],
            'word': word
        }
        if include_extra:
            try:
                extra = {
                    'orig_form': response['word_forms'][0],
                    'pic_url': response['pic_url'],
                    'sound_url': response['sound_url']
                }
                word_info.update(extra)
            except IndexError:
                print("EXEPTION: ", "{0} has no Extra".format(word))
        return word_info

    @classmethod
    def translate(self, word):
        import re

        twords = self.get_lingualeo_data(word, False)['twords']
        for t in twords:
            if re.search('[а-яА-Я]', t): return t
        return ''

    @classmethod
    def insert_to_top(self, element, array):
        if element in array:
            t_index = array.index(element)
            array.pop(t_index)
            array.insert(0, element)

    @classmethod
    def parse(self, words):
        """Example
        input = ['поддерживать',
                 'обеспечивать',
                 'поддерживать',
                 'поддерживать (морально и материально), придавать силы, способствовать {uphold}; испытывать; нести; переносить; подтверждать, подкреплять (теорию) {confirm, corroborate}; быть опорой, подпирать {support, prop up}; исполнять, выдерживать (роль)',
                 'подтверждать']
        """
        import re

        temp = set()
        for val in words:
            val = re.sub(r'[\({](.*?)[}\)]', '', val) # delete everything in parentheses
            val = re.split(',|;', val)
            val = map(lambda x: x.strip(), val) # delete whitespace around the edges
            [ temp.add(each) for each in filter(None, val) ]

        return list(temp)

    @classmethod
    def dowload(self, url):
        if not url:
            return ''

        file_name = url.split('/')[-1]
        file_path = path.join(MEDIA_DIR_PATH, file_name)
        if not path.isfile(file_path): # there no need to rewrite the file
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
        return file_name

    @classmethod
    def unique(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

    @classmethod
    def distinguish(self, word, sentence):
        return sentence.replace(word, "<b>" + word + "</b>")

    @classmethod
    def context_example(self, term, amount):
        from bs4 import BeautifulSoup

        try:
            url = "http://dictionary.reference.com/browse/{0}".format(term)
            data = BeautifulSoup(requests.get(url).text, "html.parser")
            terms = data.find_all(class_ = "partner-example-text")[-amount:] # last 2 terms is "Historical Examples"
            return [t.getText().replace("\n", "") for t in terms]
        except Exception as e:
            print("EXEPTION: ", "{0} has no Synonyms in the API".format(term))
            if DEBUG : print(e)
            return []

if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file_path", default=FILE_PATH,
                      help="write word data to FILE", metavar="FILE")
    parser.add_argument("-i", "--images", dest="image_dir_path", default=MEDIA_DIR_PATH,
                      help="save images to DIRECTORY", metavar="FILE")
    parser.add_argument("-j", "--join", dest="join_symbol", default=JOIN_SYMBOL,
                      help="a symbol which connects up words")
    opts = parser.parse_args()

    server_address = ('127.0.0.1', 3100)
    FILE_PATH = path.abspath(opts.file_path)
    MEDIA_DIR_PATH = path.abspath(opts.image_dir_path)
    JOIN_SYMBOL = opts.join_symbol

    if not path.isfile(FILE_PATH) : open(FILE_PATH, 'a').close()  # create if doesn't exist
    if not path.isdir(MEDIA_DIR_PATH) : sys.exit("%s is wrong path to save images" % MEDIA_DIR_PATH)

    if DEBUG : print("DEBUG: ", "Word data will be writen to %s" % FILE_PATH, file=sys.stderr)
    if DEBUG : print("DEBUG: ", "Images will be saved to %s" % MEDIA_DIR_PATH, file=sys.stderr)

    httpd = HTTPServer(server_address, Handler)
    if DEBUG : print("DEBUG: ", 'http server is running...listening on port %s' % server_address[1], file=sys.stderr)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)