import asyncio
import websockets


async def test_websocket():
    uri = "ws://localhost:8000/ws?pair=BTCUSDT"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(response)

asyncio.run(test_websocket())
