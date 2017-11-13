import sys
import shutil
from argparse import ArgumentParser
from os import path
import fileinput

home = path.expanduser("~")

default_path = ".config/google-chrome/Default/Extensions/nglbhlefjhcjockellmeclkcijildjhi/2.0.3.3_0"

def main():
    parser = ArgumentParser(description="save patched extention to DIR")

    parser.add_argument("get_from", metavar="DIR",
                        default=path.join(home, default_path), nargs="?")

    parser.add_argument("save_to", metavar="DIR",
                        default=path.join(home, 'Downloads/lingualeo-patched'), nargs="?")

    opts = parser.parse_args()

    if not path.isdir(opts.get_from):
        sys.exit("{} is wrong path to extention".format(opts.save_to))

    print("-- Patched extention from", opts.get_from)
    print("-- Patched extention will be saved to", opts.save_to)

    if path.isdir(opts.save_to):
        shutil.rmtree(opts.save_to)

    shutil.copytree(opts.get_from, opts.save_to, ignore=shutil.ignore_patterns('_metadata'))

    textToSearch = "g+lingualeo.config.ajax.addWordToDict"
    textToReplace = "\"http://localhost:3000\""

    fileToSearch = path.join(opts.save_to, 'lingualeo/js/server.js')

    with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(textToSearch, textToReplace), end='')

if __name__ == '__main__':
    main()
