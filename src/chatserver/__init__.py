import asyncio

from typing import NoReturn
from quart import Quart, render_template, websocket

from .broker import Broker

app = Quart(__name__)
broker = Broker()


def run():
    app.run()


@app.get("/")
async def index():
    return await render_template("index.html")


async def _send() -> NoReturn:
    async for message in broker.subscribe():
        await websocket.send(message)


async def _receive() -> NoReturn:
    while True:
        message = await websocket.receive()
        await broker.publish(message)


@app.websocket("/ws")
async def ws():
    producer = asyncio.create_task(_send())
    consumer = asyncio.create_task(_receive())

    await asyncio.gather(producer, consumer)
