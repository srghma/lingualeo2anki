#!/usr/bin/python

import re
import sys
import os
import subprocess

filename = os.path.abspath(sys.argv[1])

try:
    content = open(filename).read()
except UnicodeDecodeError as e:
    content = open(filename, encoding='iso-8859-1').read()


content = re.sub(r'\d*\n.*-->.*\n', '', content)
content = re.sub(r'<[^>]+>', '', content)
content = re.sub(r'(.)\n([^-\n])', '\g<1> \g<2>', content)
content = re.sub(r'([\w,])\n\n(.)', '\g<1> \g<2>', content)
content = re.sub(r'\.\.\.\n\n', ' ', content)

filename_txt = os.path.splitext(filename)[0]+'.txt'
file_txt = open(filename_txt, "w")
file_txt.write(content)
file_txt.close()

subprocess.Popen(["google-chrome-stable", filename_txt], start_new_session=True)
subprocess.Popen(["subl3", filename_txt], start_new_session=True)
subprocess.Popen(["subl3", "/home/bjorn/anki.csv"], start_new_session=True)
