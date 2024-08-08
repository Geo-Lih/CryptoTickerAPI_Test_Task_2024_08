import json
import websockets
from typing import Optional
from fastapi import WebSocket

from exchanges.base import BaseExchange
from constants import (
    BINANCE_PAIR_WEBSOCKET_URL,
    BINANCE_ALL_PAIRS_WEBSOCKET_URL, EXCHANGE_KEYS, BINANCE)


class BinanceExchange(BaseExchange):
    """
    Handles WebSocket connection to Binance and processes ticker data.
    """
    def __init__(self, websocket: WebSocket, pair: Optional[str] = None):
        super().__init__(websocket, BINANCE)
        self.pair = pair

    async def start(self):
        uri = self._get_websocket_uri(self.pair)
        async with websockets.connect(uri) as ws:
            while True:
                message = await ws.recv()
                await self.process_message(message)

    async def process_message(self, message: str):
        data = self._parse_message(message)
        for ticker in data:
            if self._is_valid_ticker(ticker):
                avg_price = self._calculate_average_price(ticker)
                await self.send_data(
                    BINANCE,
                    ticker[self.symbol_key],
                    avg_price,
                    float(ticker[self.bid_key]),
                    float(ticker[self.ask_key])
                )

    @staticmethod
    def _get_websocket_uri(pair: Optional[str]) -> str:
        if pair:
            return BINANCE_PAIR_WEBSOCKET_URL.format(pair.lower())
        return BINANCE_ALL_PAIRS_WEBSOCKET_URL

    @staticmethod
    def _parse_message(message: str) -> list:
        data = json.loads(message)
        return [data] if isinstance(data, dict) else data

    @staticmethod
    def _is_valid_ticker(ticker: dict) -> bool:
        return all(key in ticker for key in EXCHANGE_KEYS[BINANCE].values())

    def _calculate_average_price(self, ticker: dict) -> float:
        return (float(ticker[self.bid_key]) + float(ticker[self.ask_key])) / 2
