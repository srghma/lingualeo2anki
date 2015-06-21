#!/usr/bin/env python
from scapy.all import *
import sys
import urllib
import requests
import simplejson as json
from os import path, getcwd
from pprintpp import pprint as pp

FILE_PATH = path.join(os.getcwd(), 'anki.csv')
IMAGE_DIR_PATH = path.join(path.expanduser('~'), 'Documents', 'Anki', 'User 1', 'collection.media')
JOIN_SYMBOL = '|'

SUPPORT_HTML = True
SAVE_PICTURES = True

def handle(package):
    #parsing package if it have data, else - exit from func
    if not package.haslayer(Raw): return
    raw = str(package.getlayer(Raw).load)
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

    FILE_PATH = path.abspath(opts.file_path)
    IMAGE_DIR_PATH = path.abspath(opts.image_dir_path)
    JOIN_SYMBOL = opts.join_symbol
    SUPPORT_HTML = opts.support_html
    SAVE_PICTURES = opts.save_pictures

    if (not path.isfile(FILE_PATH)):
        open(FILE_PATH, 'a').close()  # create if doesn't exist
    if (not path.isdir(IMAGE_DIR_PATH)):
        sys.exit("Wrong path to save images")

    try:
        filter = "dst host 54.194.119.184"
        # filter = "dst api.lingualeo.com"
        sniff(iface="wlp3s0", filter=filter, prn=handle)
    except KeyboardInterrupt:
        sys.exit(0)
