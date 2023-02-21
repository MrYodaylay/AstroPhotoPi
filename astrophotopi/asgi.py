class ASGIApplication:

    async def __call__(self, scope, receive, send):
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'text/plain'),
                (b'content-length', b'5'),
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'hello',
        })

