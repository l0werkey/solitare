from enums import Suit, Rank, Color
from pile_part import create_pile

class Foundation:
    def __init__(self, type: Suit):
        self.type = type
        self.pile = None

    def can_place_card(self, card):
        if self.pile is None:
            return card.rank == Rank.ACE and card.suit == self.type
        return card.suit == self.type and card.rank.value == self.pile.get_last().get_card().rank.value + 1

    def is_finished(self):
        if self.pile is None:
            return False
        return self.pile.get_last().get_card().rank == Rank.KING

class Foundations:
    def __init__(self):
        self.foundations = {suit: Foundation(suit) for suit in Suit}

    def can_place_card(self, card):
        foundation = self.foundations.get(card.suit)
        if foundation is None:
            return False
        return foundation.can_place_card(card)

    def attempt_place_card(self, card):
        foundation = self.foundations.get(card.suit)
        if foundation is None:
            return False
        if foundation.can_place_card(card):
            if foundation.pile is None:
                foundation.pile = create_pile(card)
            else:
                foundation.pile.add_card(card)
            return True
        return False
