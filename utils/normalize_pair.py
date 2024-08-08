import re
from typing import Optional

from constants import KRAKEN


def normalize_pair(pair: Optional[str], exchange: Optional[str] = None) -> Optional[str]:
    if pair is None:
        return None

    normalized = re.sub(r'[^A-Za-z0-9]', '', pair).upper()
    if exchange == KRAKEN:
        normalized = normalized.replace('XBT', 'BTC')
    else:
        normalized = normalized.replace('BTC', 'XBT')

    return normalized
