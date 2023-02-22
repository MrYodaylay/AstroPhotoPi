import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(b"Hello World")


class CustomHTTPServer:
    server_thread: Thread
    server_object: HTTPServer

    def __init__(self, address: str, port: int, request_handler=CustomHTTPRequestHandler):

        self.server_object = HTTPServer((address, port), request_handler)

    def serve_forever(self) -> None:
        self.server_thread = Thread(
            target=self._serve_forever,
            name="HTTP",
        )
        self.server_thread.start()

    def _serve_forever(self):
        addr, port = self.server_object.server_address
        logging.info(f"Listening at http://{addr}:{port}/")

        self.server_object.serve_forever()

    def join(self, timeout: Optional[float] = None):
        if self.server_thread is not None:
            self.server_thread.join(timeout)
