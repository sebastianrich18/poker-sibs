from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class Suit(str, Enum):
    hearts = "h"
    diamonds = "d"
    clubs = "c"
    spades = "s"


class Rank(str, Enum):
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    nine = "9"
    ten = "T"
    jack = "J"
    queen = "Q"
    king = "K"
    ace = "A"


class ActionType(str, Enum):
    fold = "fold"
    call = "call"
    raise_ = "raise"
    check = "check"


class Card(BaseModel):
    rank: Rank
    suit: Suit


class Deck(BaseModel):
    cards: List[Card] = Field(default_factory=list)

    def shuffle(self) -> None:
        import random

        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()
