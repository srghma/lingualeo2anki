import sys
from argparse import ArgumentParser
from http.server import HTTPServer
from os import path

from .handler import Handler
from .config import config
from .utils import debug

if __name__ == '__main__':
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

    config.write_to_path   = opts.write_to_path
    config.images_dir_path = opts.images_dir_path
    config.join_symbol     = opts.join_symbol
    config.port            = opts.port
    config.debug           = opts.debug

    print(config.__dict__)
    # create file if doesn't exist
    if not path.isfile(config.write_to_path):
        open(config.write_to_path, 'a').close()

    if not path.isdir(config.images_dir_path):
        sys.exit("%s is wrong path to save images" % config.images_dir_path)

    debug("Word data will be writen to %s", config.write_to_path)
    debug("Images will be saved to %s", config.images_dir_path)

    httpd = HTTPServer(config.server_address, Handler)
    debug('http server is running...listening on port %s', config.port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit(0)
