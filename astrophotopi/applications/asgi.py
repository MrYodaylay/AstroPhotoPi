
class Asgi():

    static_directory : str = ""
    camera = None

    async def __call__(self, scope, receive, send):

        if scope["type"] in ["http", "https"]:

            if scope["method"] == "GET":

                path = scope["path"]
                if path is None or path == "":
                    path = "index.html"

                if scope["path"].startswith("/api"):

                    if scope["path"] == "/api/cameras":
                        data = self.camera.get_name()
                        code = 200
                        content_type = "text/json"
                    else:
                        data = "File Not Found"
                        code = 404
                        content_type = "text/plain"


                else:

                    full_path = self.static_directory + scope["path"]
                    print(full_path)

                    try:
                        with open(full_path, "r") as file:
                            data = file.read()
                            code = 200

                            if (full_path.endswith(".js")):
                                content_type = "text/javascript"
                            else:
                                content_type = "text/html"
                    except Exception as e:
                        data = "File Not Found"
                        code = 404
                        content_type = "text/plain"

                await send({
                    'type': 'http.response.start',
                    'status': code,
                    'headers': [
                        (b'content-type', content_type.encode("utf-8")),
                        (b'content-length', str(len(data)).encode("utf-8")),
                    ],
                })
                await send({
                    'type': 'http.response.body',
                    'body': data.encode("utf-8"),
                })

            else:
                await send({
                    'type': 'http.response.start',
                    'status': 405,
                    'headers': [
                        (b'content-type', b'text/plain'),
                        (b'content-length', b'18'),
                    ],
                })
                await send({
                    'type': 'http.response.body',
                    'body': b'Method Not Allowed',
                })

