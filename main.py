from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import asyncio
from exchanges.connector import ExchangeConnector
from typing import Optional
from utils.determine_exchanges import determine_exchanges
from utils.normalize_pair import normalize_pair

app = FastAPI()
connector = ExchangeConnector()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             pair: Optional[str] = Query(None),
                             exchange: Optional[str] = Query(None)):
    """
    Handle WebSocket connection and start relevant exchanges.
    """

    await websocket.accept()
    try:
        # await connector.stop_connections()

        normalized_pair = normalize_pair(pair, exchange)
        exchanges_to_start = determine_exchanges(exchange)
        tasks = [connector.start(exchange_cls, websocket, normalized_pair) for exchange_cls in exchanges_to_start]
        await asyncio.gather(*tasks)

    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
