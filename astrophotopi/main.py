import asyncio
import threading
import time

from hypercorn.asyncio import serve
from hypercorn.config import Config

from astrophotopi import AstroPhotoPi
from astrophotopi import ASGIApplication


def server_thread():

    # Set up asyncio loop
    loop = asyncio.new_event_loop()

    # Create hypercorn coroutine
    asgi = ASGIApplication()
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    server = serve(asgi, config)

    loop.create_task(server)

    loop.run_forever()

def main():

    thread = threading.Thread(target=server_thread)
    thread.start()

    print("Main continues")
    time.sleep(5)
    print("Exiting")


if __name__ == "__main__":
    main()

