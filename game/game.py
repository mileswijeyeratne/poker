from typing import Dict, List, Optional
from enum import Enum, auto

from .card import Card
from .deck import Deck
from .player import Player

class GameState(Enum):
    WAITING = auto()
    PLAYING = auto()
    FINISHED = auto()

class PokerGame:
    MIN_PLAYERS = 4
    MAX_PLAYERS = 8

    def __init__(self) -> None:
        self.__deck = Deck()
        self.__players: Dict[int, Player] = {}
        self.__state = GameState.WAITING
        self.__river: Optional[List[Card]] = None
        self.__turn: Optional[Card] = None
        self.__flop: Optional[Card] = None

        print(f"[Game] initialized a new game")

    @property
    def is_full(self) -> bool:
        return len(self.__players) >= self.MAX_PLAYERS

    def add_player(self, name: str, id: int) -> None:
        if id in self.__players:
            raise ValueError("player with that id already exists in the game")

        self.__players[id] = Player(name)

        print(f"[Game] added player {name} (id: {id}) to game")

        if self.is_full:
            self.start()

    def remove_player(self, id: int) -> None:
        if self.__state == GameState.PLAYING:
            # TODO: make player fold
            pass
        del self.__players[id]

    def start(self)-> None:
        assert len(self.__players) >= self.MIN_PLAYERS, f"cannot start game with less than {self.MIN_PLAYERS} players"

        self.__deck.shuffle()
        self.__state = GameState.PLAYING
        self.__deal()
    
    def __deal(self)-> None:
        for p in self.__players.values():
            p.give_card(self.__deck.draw_card())
            p.give_card(self.__deck.draw_card())

    def reset(self)-> None:
        self.__deck.reset()
        for p in self.__players.values():
            p.empty_hand()
        self.__river = None
        self.__turn = None
        self.__flop = None
        self.__state = GameState.WAITING

    def process_request(self, request: Dict, id: Player) -> Dict:
        """
        API IMPLEMENTATION
        """
        # TODO IMPLEMENT
        print(f"[GAME] got request {request} from {self.__players[id]} (id: {id})")
        return {"type": "OK"}
    

if __name__ == "__main__":
    g = PokerGame()
    g.add_player("Miles", 1)
    g.add_player("Fabs", 2)
    g.add_player("Daniel", 3)
    g.add_player("AoQun", 4)

    print(g._PokerGame__players)
    g.start()
    print(g._PokerGame__players)
    g.reset()
    print(g._PokerGame__players)