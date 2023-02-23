import logging
import time

from astrophotopi import CustomHTTPServer, CustomHTTPRequestHandler


def main():

    print("AstroPhotoPi starting")

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)6d [%(threadName)s] %(message)s")

    server = CustomHTTPServer("0.0.0.0", 8080)
    server.serve_forever()

    logging.debug("Main continuing")

    server.join()


if __name__ == "__main__":
    main()

