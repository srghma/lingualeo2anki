import sys
from argparse import ArgumentParser
from http.server import HTTPServer
from os import path

from .handler import Handler
from .config import config
from .utils import debug


def main():
    parser = ArgumentParser()

    parser.add_argument("-f", "--file", dest="write_to_path",
                        help="write word data to FILE", metavar="FILE",
                        default=config.write_to_path)

    parser.add_argument("-i", "--images", dest="images_dir_path",
                        help="save images to DIRECTORY", metavar="FILE",
                        default=config.images_dir_path)

    parser.add_argument("-j", "--join", dest="join_symbol",
                        default=config.join_symbol)

    parser.add_argument("-p", dest="port",
                        default=config.port)

    parser.add_argument("--debug", action='store_true', dest="debug",
                        default=config.debug)

    opts = parser.parse_args()

    config.update(opts)

    # create file if doesn't exist
    if not path.isfile(config.write_to_path):
        open(config.write_to_path, 'a').close()

    if not path.isdir(config.images_dir_path):
        sys.exit("%s is wrong path to save images" % config.images_dir_path)

    debug("Word data will be writen to %s", config.write_to_path)
    debug("Images will be saved to %s", config.images_dir_path)

    try:
        httpd = HTTPServer(config.server_address, Handler)
        debug('http server is running...listening on port %s', config.port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)
    finally:
        debug("finnaly")
        httpd.server_close()
        sys.exit(0)


if __name__ == '__main__':
    main()
