from typing import Optional, Type

from constants import BINANCE, KRAKEN
from exchanges.base import BaseExchange
from exchanges.binance import BinanceExchange
from exchanges.kraken import KrakenExchange


def determine_exchanges(exchange: Optional[str]) -> list[Type[BaseExchange]]:
    """
    Determines exchanges to connect to based on the `exchange` parameter.
    """

    if exchange == BINANCE:
        return [BinanceExchange]
    elif exchange == KRAKEN:
        return [KrakenExchange]
    else:
        return [KrakenExchange, BinanceExchange]
