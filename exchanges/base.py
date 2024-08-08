import json
from fastapi import WebSocket

from constants import EXCHANGE_KEYS


class BaseExchange:
    """
    Base class for handling WebSocket connections to exchanges.

    Methods:
    - _initialize_keys: Initializes exchange-specific keys for bid, ask, and symbol.
    - send_data: Sends formatted ticker data via WebSocket.
    """
    def __init__(self, websocket: WebSocket, exchange_name: str):
        self.websocket = websocket
        self.exchange_name = exchange_name
        self._initialize_keys()

    def _initialize_keys(self):
        self.keys = EXCHANGE_KEYS[self.exchange_name]
        self.bid_key = self.keys['bid']
        self.ask_key = self.keys['ask']
        self.symbol_key = self.keys['symbol']

    async def send_data(self, exchange: str, pair: str, avg_price: float, bid_price: float, ask_price: float):
        await self.websocket.send_text(
            json.dumps({
                "exchange": exchange,
                "pair": pair,
                "avg_price": avg_price,
                "bid_price": bid_price,
                "ask_price": ask_price,
            })
        )
