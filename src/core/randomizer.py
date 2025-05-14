from enums import Suit, Rank, Color
import random

def get_random_from_enum(enum_cls):
    return random.choice(list(enum_cls))

get_random_suit = lambda: get_random_from_enum(Suit)
get_random_rank = lambda: get_random_from_enum(Rank)