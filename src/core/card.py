from enums import Suit, Rank, Color
from randomizer import get_random_suit, get_random_rank

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def is_rank_higher(self, other_card: 'Card') -> bool:
        return self.rank.value > other_card.rank.value
    
    def is_same_suit(self, other_card: 'Card') -> bool:
        return self.suit == other_card.suit
    
    def is_same_color(self, other_card: 'Card') -> bool:
        return self.get_color() == other_card.get_color()
    
    def get_color(self):
        return Color.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Color.BLACK

    def __str__(self):
        return f"{self.rank.name} of {self.suit.name} ({self.get_color().name})"
    
    def clone(self) -> 'Card':
        return Card(self.suit, self.rank)
    
def create_card(suit=None, rank=None) -> Card:
    return Card(
        suit or get_random_suit(),
        rank or get_random_rank(),
    )