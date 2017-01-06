import sys
from argparse import ArgumentParser
from http.server import HTTPServer
from os import path
import signal

from .handler import Handler
from .config import config
from .utils import debug


def main():
    parser = ArgumentParser()

    parser.add_argument("-f", "--file", dest="output_file_path",
                        help="write word data to FILE", metavar="FILE",
                        default=config.output_file_path)

    parser.add_argument("-m", "--media", dest="media_dir_path",
                        help="save images and sound to DIRECTORY", metavar="FILE",
                        default=config.media_dir_path)

    parser.add_argument("-j", "--join", dest="join_symbol",
                        default=config.join_symbol)

    parser.add_argument("-p", dest="port",
                        default=config.port)

    parser.add_argument("--debug", action='store_true', dest="debug",
                        default=config.debug)

    parser.add_argument("--silent", action='store_true', dest="silent",
                        default=config.silent)

    opts = parser.parse_args()

    config.update(opts)

    if not path.isdir(config.media_dir_path):
        sys.exit("{} is wrong path to save images".format(config.media_dir_path))

    debug("Word data will be writen to {}", config.output_file_path)
    debug("Images will be saved to {}", config.media_dir_path)

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
