import json
import websockets
import requests
from typing import Optional
from fastapi import WebSocket

from exchanges.base import BaseExchange
from constants import (KRAKEN_ASSET_PAIRS_URL, KRAKEN_WEBSOCKET_URL, KRAKEN)
from utils.long_list_yield import long_list_yield
from utils.normalize_pair import normalize_pair


class KrakenExchange(BaseExchange):
    """
    Handles WebSocket connection to Kraken and processes ticker data.

    Methods:
    - start: Connects to Kraken WebSocket and processes incoming messages.
    - process_message: Processes and sends ticker data from received messages.
    - _get_pairs: Retrieves the list of trading pairs.
    - _pairs: Property that returns the trading pairs for the WebSocket connection.
    - _subscribe_to_pairs: Subscribes to the specified trading pairs on Kraken.
    - _is_ticker_data: Checks if the data is ticker information.
    """
    def __init__(self, websocket: WebSocket, pair: Optional[str] = None):
        super().__init__(websocket, KRAKEN)
        self.pair = pair

    async def start(self):
        pairs = self._get_pairs()
        async with websockets.connect(KRAKEN_WEBSOCKET_URL) as ws:
            await self._subscribe_to_pairs(ws, pairs)
            while True:
                message = await ws.recv()
                await self.process_message(message)

    async def process_message(self, message: str):
        data = json.loads(message)
        if self._is_ticker_data(data):
            for ticker in data['data']:
                avg_price = self._calculate_average_price(ticker)
                formatted_pair = normalize_pair(ticker[self.symbol_key])
                await self.send_data(
                    KRAKEN,
                    formatted_pair,
                    avg_price,
                    float(ticker[self.bid_key]),
                    float(ticker[self.ask_key])
                )

    def _get_pairs(self) -> list[str]:
        return self._pairs

    @property
    def _pairs(self) -> list[str]:
        response = requests.get(KRAKEN_ASSET_PAIRS_URL)
        data = response.json()
        if self.pair:
            return [pair_info['wsname'] for pair_info in data['result'].values() if pair_info['altname'] == self.pair]
        return [pair_info['wsname'] for pair_info in data['result'].values()]

    @staticmethod
    async def _subscribe_to_pairs(ws, pairs):
        for batch_pairs in long_list_yield(pairs):
            await ws.send(json.dumps({
                "method": "subscribe",
                "params": {
                    "channel": "ticker",
                    "symbol": batch_pairs
                }
            }))

    @staticmethod
    def _is_ticker_data(data: dict) -> bool:
        return data.get("channel") == "ticker" and "data" in data and len(data["data"]) > 0
