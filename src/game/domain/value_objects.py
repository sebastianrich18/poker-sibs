from abc import ABC

from game.domain.enums import Suit, Rank


class GameAction(ABC):
    pass


class Card:
    rank: Rank
    suit: Suit
