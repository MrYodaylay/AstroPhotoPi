import logging
from typing import Dict, Tuple, Any, Optional, Callable, BinaryIO
from dataclasses import dataclass
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler


@dataclass
class HTTPRequest:
    path: str


@dataclass
class HTTPResponse:
    _response_code: Callable[[int, str], Any]
    _response_headers: Callable[[str, str], Any]
    _response_body: BinaryIO

    def send_response(self, code: int, message: str):
        self._response_code(code, message)

    def send_headers(self, keyword: str, value: str):
        self._response_headers(keyword, value)

    def send_body(self, body: bytes):
        self._response_body.write(body)


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    routes: Dict[Tuple[str, str], Any] = {}

    def do_GET(self):
        route_descriptor = (self.path, "GET")
        request = HTTPRequest(self.path)
        response = HTTPResponse(self.send_response, self.send_header, self.wfile)

        if route_descriptor in self.routes:
            self.routes[route_descriptor](self)
            self.send_response(200, "OK")
            self.wfile.write(b"")
        else:
            self.send_error(404)
            self.end_headers()


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
