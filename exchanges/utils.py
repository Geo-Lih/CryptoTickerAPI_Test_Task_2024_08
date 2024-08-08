from constants import BINANCE, KRAKEN


def format_pair(pair: str, exchange: str) -> str:
    """
    Formats the pair as 'AAABBB' for Kraken
    and replaces 'XBT' with 'BTC' for Kraken.
    """
    if exchange == BINANCE:
        #.
        return pair
    if exchange == KRAKEN:
        return pair.replace('XBT', 'BTC').replace('/', '')
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")

