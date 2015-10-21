#!/usr/bin/env python
import requests
import simplejson as json
from os import path
from http.server import SimpleHTTPRequestHandler, HTTPServer
import pprint; from pprintpp import pprint as pp
from PyDictionary import PyDictionary; dictionary=PyDictionary()

DEBUG = True
FILE_PATH = path.join(path.dirname(path.realpath(__file__)), 'anki.csv')
MEDIA_DIR_PATH = path.join( path.expanduser("~"), 'Documents', 'Anki', 'User 1', 'collection.media')
JOIN_SYMBOL = '|'

<<<<<<< HEAD
SUPPORT_HTML = True
SAVE_PICTURES = True

def handle(package):
    #parsing package if it have data, else - exit from func
    if not package.haslayer(Raw): return
    try:
        raw = str(package.getlayer(Raw).load.decode("utf-8"))
    except UnicodeDecodeError as e:
        return
    
    if "word" not in raw or not "context" in raw: return
    s = raw.lstrip("b'").rstrip("'").split("&")  # delete b' on  and '
    try:
        request_word = s[0].split("=")[-1].strip()
        context = s[2].split("=")[-1].strip()
    except Exception as e:
        print(e)
        print('s =', s)
        return

    data = {
        "request_word": request_word,
        "context": context,
        "word": '',
        "type": '',
        "translations": '',
        "transcription": '',
        "pic_name": '',
        "sound_url": ''  # for future
    }

    #HTML support
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

def get_word_info(word, host="https://api.lingualeo.com/gettranslates", include_media=1, add_word_forms=1):
    data = {
        'word': word,
        'include_media': include_media,
        'add_word_forms': add_word_forms
    }
    return requests.post(host, data).json()

def dowload_pic(pic_url, pic_name):
    dir_path = IMAGE_DIR_PATH
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
=======
class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        intercept = self.get_interception()

        # if word have different orig form - take data from orig_form
        if not intercept['orig_form'] or intercept['word'] == intercept['orig_form']['word']:
            templ = intercept
        else:
            templ = Helper.get_lingualeo_data(intercept['orig_form']['word'])

        if intercept['context']:
            context = Helper.context_example(templ['word'], 2)
            context = Helper.distinguish(templ['word'], context )

            user_selected_transl = intercept['twords'][0]
            intercept_context = intercept['context'].replace(intercept['word'], intercept['word'] + "(" + user_selected_transl + ")")
            intercept_context = Helper.distinguish(intercept['word'], intercept_context )

            context.insert(0, intercept_context)
        else:
            context = Helper.context_example(templ['word'], 3)
            context = Helper.distinguish(templ['word'], context )

        templ['twords'] = Helper.unique(templ['twords'])
        try:
            data = {
                'word':              templ['word'],
                'twords':            ', '.join(templ['twords']),
                'transcr':           templ['transcr'],
                'pic_name':          Helper.dowload(templ['pic_url']),
                # 'sound_name':        Helper.dowload(templ['sound_url']),
                'context':           "<br><br>".join(context),
                'synonyms':          '',
                'synonyms_&_transl': '',
            }

            if len( templ['word'].split(' ') ) <= 1:
                synonyms = { key: Helper.translate(key) for key in dictionary.synonym(templ['word']) }
                data['synonyms'] = ', '.join( synonyms.keys() )
                data['synonyms_&_transl'] = ', '.join([key+'('+value+')' for key, value in synonyms.items()])

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
                'word':    word,
                'transcr': transl['transcr'],
                'twords':  transl['twords'],
            }

            interception['context']       = " ".join(body['context']).replace('\n', '') if 'context' in body else ''
            interception['context_title'] = body.get('context_title', [''])[0]
            interception['context_url']   = body.get('context_url', [''])[0]
            interception['orig_form']     = transl.get('orig_form', '')
            interception['pic_url']       = transl.get('pic_url', '')
            interception['sound_url']     = transl.get('sound_url', '')
        except Exception as e:
            pp(body)
            raise e

        Helper.locate_to_top(body['tword'][0], interception['twords'])
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
            'twords': [ t['value'].replace('\n', ' ') for t in response['translate'] ],
            'word': word
        }
        if include_extra:
            try:
                if response['word_forms']: word_info['orig_form'] = response['word_forms'][0]
                word_info['pic_url']   = response.get('pic_url', '')
                word_info['sound_url'] = response.get('sound_url', '')
            except Exception as e:
                pp(response)
                raise e
        return word_info

    @classmethod
    def translate(self, word):
        import re

        twords = self.get_lingualeo_data(word, False)['twords']
        for t in twords:
            if re.search('[а-яА-Я]', t): return t
        return ''

    @classmethod
    def locate_to_top(self, element, array):
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
        for word in words:
            word = re.sub(r'[\({](.*?)[}\)]', '', word) # delete everything in parentheses
            word = re.split(',|;', word)
            word = map(lambda x: x.strip(), word) # delete whitespace around the edges
            [ temp.add(each) for each in filter(None, word) ]

        return list(temp)

    @classmethod
    def dowload(self, url):
        if not url: return ''

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
        try:
            return sentence.replace(word, "<b>" + word + "</b>")
        except AttributeError:
            return [x.replace(word, "<b>" + word + "</b>") for x in sentence]

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
>>>>>>> server

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
<<<<<<< HEAD
    parser.add_argument("--nopic", action="store_false", dest="save_pictures", default=SAVE_PICTURES,
                      help="don't save pictures in folder (Anki folder in default)")
=======
>>>>>>> server
    opts = parser.parse_args()

    server_address = ('127.0.0.1', 3100)
    FILE_PATH = path.abspath(opts.file_path)
    MEDIA_DIR_PATH = path.abspath(opts.image_dir_path)
    JOIN_SYMBOL = opts.join_symbol
<<<<<<< HEAD
    SAVE_PICTURES = opts.save_pictures
=======
>>>>>>> server

    if not path.isfile(FILE_PATH) : open(FILE_PATH, 'a').close()  # create if doesn't exist
    if not path.isdir(MEDIA_DIR_PATH) : sys.exit("%s is wrong path to save images" % MEDIA_DIR_PATH)

    if DEBUG : print("DEBUG: ", "Word data will be writen to %s" % FILE_PATH, file=sys.stderr)
    if DEBUG : print("DEBUG: ", "Images will be saved to %s" % MEDIA_DIR_PATH, file=sys.stderr)

    httpd = HTTPServer(server_address, Handler)
    if DEBUG : print("DEBUG: ", 'http server is running...listening on port %s' % server_address[1], file=sys.stderr)

<<<<<<< HEAD
    print("Word data will be writen to %s" % FILE_PATH)
    print("Images will be saved to %s" % IMAGE_DIR_PATH)
    try:
        sniff(iface="wlp3s0", filter='tcp port 80', prn=handle)
=======
    try:
        httpd.serve_forever()
>>>>>>> server
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)