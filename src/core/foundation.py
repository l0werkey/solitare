from enums import Suit, Rank
from card import Card

class Foundation:
    def __init__(self):
        self.piles = {suit: [] for suit in Suit}

    def add_card(self, card: Card) -> bool:
        target_pile = self.piles[card.suit]
        if (not target_pile and card.rank == Rank.ACE) or \
           (target_pile and card.rank == target_pile[-1].rank + 1):
            target_pile.append(card)
            return True
        return False