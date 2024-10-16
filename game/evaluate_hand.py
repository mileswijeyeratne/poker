from typing import List
from enum import Enum
from functools import total_ordering

from .card import Card

@total_ordering
class HandValue(Enum):
    NO_PAIR = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_KIND = 7
    STRAIGHT_FLUSH = 8

    def __lt__(self, other) -> bool:
        if not isinstance(other, HandValue):
            raise NotImplementedError("Cannot compare hand value to abject of different type")
        return self.value < other.value

def evaluate(hand: List[Card]) -> HandValue:
    pass