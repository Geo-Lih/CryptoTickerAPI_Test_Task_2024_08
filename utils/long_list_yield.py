from typing import List
from constants import BATCH_SIZE


def long_list_yield(value_list: List[str], split_coef: int = BATCH_SIZE) -> List[List[str]]:
    """Splits a list into batches of size split_coef."""
    return [value_list[i:i + split_coef] for i in range(0, len(value_list), split_coef)]
