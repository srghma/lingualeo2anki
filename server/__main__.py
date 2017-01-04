import sys
from argparse import ArgumentParser
from http.server import HTTPServer
from os import path
import signal

from .handler import Handler
from .config import config
from .utils import debug, create_file


def main():
    parser = ArgumentParser()

    parser.add_argument("-f", "--file", dest="csv_path",
                        help="write word data to FILE", metavar="FILE",
                        default=config.csv_path)

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

    create_file(config.csv_path)

    if not path.isdir(config.images_dir_path):
        sys.exit("{} is wrong path to save images".format(config.images_dir_path))

    debug("Word data will be writen to {}", config.csv_path)
    debug("Images will be saved to {}", config.images_dir_path)

    server = None

    def close_server(signum, frame):
        debug("Server was closed by system signal {}", signum)
        if server:
            server.server_close()
            sys.exit()

    server = HTTPServer(config.server_address, Handler)
    signal.signal(signal.SIGINT,  close_server)
    signal.signal(signal.SIGTERM, close_server)
    debug('Listening port {}', config.port)
    server.serve_forever()


if __name__ == '__main__':
    main()
