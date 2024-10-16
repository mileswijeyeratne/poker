from .card import Card

from typing import List

class Player:
    def __init__(self, name: str) -> None:
        self.__hand: List[Card] = []
        self.__name = name
        self.__money: int = 0

    def __str__(self):
        return f"Player<name: {self.__name}, hand: {', '.join(str(c) for c in self.__hand) if self.__hand else 'empty'}>"

    __repr__ = __str__

    @property
    def name(self) -> str:
        return self.__name

    @property
    def hand(self) -> List[Card]:
        return self.__hand
    
    @property
    def money(self) -> int:
        return self.__money 
    
    def give_card(self, card: Card) -> None:
        self.__hand.append(card)
        
    def remove_card(self, card: Card) -> None:
        """
        Removes card if it is the same instance (i.e same python id())
        """
        self.__hand = [c for c in self.__hand if c is not card]

    def empty_hand(self) -> None:
        self.__hand = []

    def give_money(self, amount: int) -> None:
        self.__money += amount

    def take_money(self, amount: int) -> None:
        if amount > self.__money:
            raise ValueError("remove more money then player has")

        self.__money -= amount

    def set_money(self, amount: int) -> None:
        self.__money = amount