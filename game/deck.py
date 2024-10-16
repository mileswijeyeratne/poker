from .card import Card, CardValue, CardSuit

from queue import Queue
from random import shuffle as _shuffle

class Deck:
    def __init__(self, shuffled=False) -> None:
        self.__cards: Queue[Card] = Queue()

        self.shuffle() if shuffled else self.reset()

    def __len__(self) -> int:
        return len(self.__cards)

    def reset(self) -> None:
        self.__cards = Queue()

        for suit in CardSuit:
            for value in CardValue:
                self.__cards.put(Card(value, suit))

    def return_card(self, card: Card) -> None: 
        self.__cards.put(card)

    def draw_card(self) -> Card:
        if self.__cards.qsize() == 0:
            raise IndexError("draw from empty deck")
        
        return self.__cards.get()

    def shuffle(self) -> None:
        cards = []

        for suit in CardSuit:
            for value in CardValue:
                cards.append(Card(value, suit))

        _shuffle(cards)

        self.__cards = Queue()
        for c in cards:
            self.__cards.put(c)