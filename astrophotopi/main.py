import asyncio
from pathlib import Path
from hypercorn.asyncio import serve
from hypercorn.config import Config

from applications import Asgi
from camera import Camera

config = Config()
config.bind = ["0.0.0.0:8080"]

app = Asgi()
app.camera = Camera()

base_directory = Path(__file__).parent.parent
static_directory = base_directory.joinpath("webapp")
app.static_directory = str(static_directory)

asyncio.run(serve(app, config))