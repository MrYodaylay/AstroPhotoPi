from dataclasses import dataclass
from typing import Callable, Any, BinaryIO

from astrophotopi.httpinterface.exception import HeadersFinishedException


@dataclass
class HTTPRequest:
    path: str


@dataclass
class HTTPResponse:
    _response_code: Callable[[int, str], Any]
    _response_headers: Callable[[str, str], Any]
    _response_body: BinaryIO

    __headers_finished = False

    def send_response(self, code: int, message: str):
        self._response_code(code, message)

    def send_headers(self, keyword: str, value: str):
        self._response_headers(keyword, value)

        # Cannot send more headers after the body has begun to be sent
        if self.__headers_finished:
            raise HeadersFinishedException()

    def send_body(self, body: bytes):
        self._response_body.write(body)
        self.__headers_finished = True
