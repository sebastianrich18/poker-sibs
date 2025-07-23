from enum import Enum


class GameType(Enum):
    POKER = "poker"

class Suit(Enum):
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'
    
class Rank(Enum):
    ACE = 'A'
    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    TEN = '10'
    NINE = '9'
    EIGHT = '8'
    SEVEN = '7'
    SIX = '6'
    FIVE = '5'
    FOUR = '4'
    THREE = '3'
    TWO = '2'