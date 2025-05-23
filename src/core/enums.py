from enum import Enum, auto

class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()

class Rank(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12

class Color(Enum):
    RED = auto()
    BLACK = auto()

class Difficulty(Enum):
    EASY = auto()
    HARD = auto()

    def __str__(self):
        return "Łatwy" if self == Difficulty.EASY else "Trudny"