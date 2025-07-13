from typing import List
from ..domain.entities import Card
import random

SUITS = ["h", "d", "c", "s"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

class Deck:
    def __init__(self):
        self.cards = [Card(rank=r, suit=s) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()
