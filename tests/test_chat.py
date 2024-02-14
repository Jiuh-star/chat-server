import asyncio

from quart.typing import TestWebsocketConnectionProtocol as _TestWebsocketConnectionProtocol

from chatserver import app


async def _receive(test_ws: _TestWebsocketConnectionProtocol) -> str:
    return await test_ws.receive()


async def test_ws():
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_ws:
        task = asyncio.create_task(_receive(test_ws))
        await test_ws.send("message")
        result = await task
        assert result == "message"

