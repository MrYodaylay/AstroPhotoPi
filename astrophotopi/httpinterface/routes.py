from astrophotopi.httpinterface.object import HTTPRequest, HTTPResponse


# def route(request, response):
#   pass


def route_index(request: HTTPRequest, response: HTTPResponse):
    response.send_response(200, "OK")
    response.send_body(b"Hello World")
