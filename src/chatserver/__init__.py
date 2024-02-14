import asyncio
from quart import Quart, render_template, websocket
from .broker import Broker

app = Quart(__name__)
broker = Broker()


async def _receive():
    while True:
        message = await websocket.receive()
        await broker.publish(message)

def run():
    app.run()


@app.get("/")
async def index():
    return await render_template("index.html")


@app.websocket("/ws")
async def ws():
    task = asyncio.create_task(_receive())

    try:
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task
