from enums import Suit, Rank, Color

class Card:
    def __init__(self, suit: Suit, rank: Rank, color: Color):
        self.suit = suit
        self.rank = rank
        self.color = color

    def is_rank_higher(self, other_card: 'Card') -> bool:
        return self.rank.value > other_card.rank.value
    
    def is_same_suit(self, other_card: 'Card') -> bool:
        return self.suit == other_card.suit
    
    def is_same_color(self, other_card: 'Card') -> bool:
        return self.color == other_card.color

    def __str__(self):
        return f"{self.rank.name} of {self.suit.name} ({self.color.name})"
    
def create_random_card() -> Card:
    import random
    suit = random.choice(list(Suit))
    rank = random.choice(list(Rank))
    color = random.choice(list(Color))
    return Card(suit, rank, color)

