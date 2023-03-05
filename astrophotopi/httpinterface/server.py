import logging
from typing import Dict, Tuple, Optional, Callable
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

from astrophotopi.httpinterface.object import HTTPRequest, HTTPResponse
from astrophotopi.httpinterface.routes import route_index


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    routes: Dict[Tuple[str, str], Callable] = {
        ("/", "GET"): route_index
    }

    def do_GET(self):
        route_descriptor = (self.path, "GET")
        self.do_ALL(route_descriptor)
    def do_POST(self):
        route_descriptor = (self.path, "POST")
        self.do_ALL(route_descriptor)

    def do_ALL(self, route_descriptor: Tuple[str, str]):
        request = HTTPRequest(self.path)
        response = HTTPResponse(self.send_response, self.send_header, self.wfile)

        if route_descriptor in self.routes:
            self.routes[route_descriptor](request, response)
            self.send_response(200, "OK")
            self.wfile.write(b"")
        else:
            self.send_error(404)
            self.end_headers()

    def register_route(self, path: str, method: str, func: Callable):
        route_descriptor = (self.path, method.upper())
        self.routes[route_descriptor] = func


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
        logging.info(f"Listening at httpinterface://{addr}:{port}/")

        self.server_object.serve_forever()

    def join(self, timeout: Optional[float] = None):
        if self.server_thread is not None:
            self.server_thread.join(timeout)
