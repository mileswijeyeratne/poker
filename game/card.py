from enum import Enum
from functools import total_ordering

@total_ordering
class CardValue(Enum):
    ACE = 14
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 20
    JACK = 11
    QUEEN = 12
    KING = 13

    def __lt__(self, other):
        if not isinstance(other, CardValue):
            raise NotImplementedError("Cannot compare card value to abject of different type")
        return self.value < other.value

@total_ordering
class CardSuit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    def __lt__(self, other):
        if not isinstance(other, CardSuit):
            raise NotImplementedError("Cannot compare card suit to abject of different type")
        return self.value < other.value


class Card:
    def __init__(self, value: CardValue, suit: CardSuit) -> None:
        self.__value = value
        self.__suit = suit

    def __str__(self) -> str:
        return f"{self.__value.name} of {self.__suit.name}"

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit