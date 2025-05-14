from enums import Suit, Rank, Color
import random

def get_random_suit() -> Suit:
    return random.choice(list(Suit))
    
def get_random_rank() -> Rank:
    return random.choice(list(Rank))

def get_random_color() -> Color:
    return random.choice(list(Color))