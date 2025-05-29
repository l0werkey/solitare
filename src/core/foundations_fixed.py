from core.enums import Suit, Rank, TransferType
from core.pile_part import create_pile

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
        
        return self.pile.get_last().get_card().rank == Rank.KING and self.pile.length() == len(Rank)
    
    def copy(self):
        new_foundation = Foundation(self.type)
        if self.pile:
            new_foundation.pile = self.pile.copy()
        return new_foundation
    
    def is_sorted(self):
        if self.pile is None:
            return False
        return self.pile.is_sorted(reversed=True)
    
    def as_list(self):
        if self.pile is None:
            return []
        return self.pile.as_list()

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

    def get_foundation(self, suit: Suit):
        return self.foundations.get(suit)

    def is_finished(self):
        for foundation in self.foundations.values():
            if not foundation.is_finished():
                return False
        return True

    def copy(self):
        new_foundations = Foundations()
        for suit, foundation in self.foundations.items():
            new_foundations.foundations[suit] = foundation.copy()
        return new_foundations

    def get_top_card(self, target_index: int):
        """Get the top card from foundation at target_index (0-3 for suits)"""
        suits = list(Suit)
        if 0 <= target_index < len(suits):
            foundation = self.foundations[suits[target_index]]
            if foundation.pile:
                return foundation.pile.get_last().get_card()
        return None

    def place_card(self, card):
        """Place a card on the appropriate foundation"""
        return self.attempt_place_card(card)

    def place_top_card(self, target_index: int):
        """Remove the top card from foundation at target_index"""
        suits = list(Suit)
        if 0 <= target_index < len(suits):
            foundation = self.foundations[suits[target_index]]
            if foundation.pile:
                if foundation.pile.next is None:
                    # Only one card, remove the pile
                    card = foundation.pile.get_card()
                    foundation.pile = None
                    return card
                else:
                    # Multiple cards, remove the last one
                    # Find second to last
                    current = foundation.pile
                    while current.next.next:
                        current = current.next
                    card = current.next.get_card()
                    current.next = None
                    return card
        return None

    def can_place_card_on_foundation(self, card, target_index: int):
        """Check if card can be placed on foundation at target_index"""
        suits = list(Suit)
        if 0 <= target_index < len(suits):
            foundation = self.foundations[suits[target_index]]
            return foundation.can_place_card(card)
        return False

    def get_type(self):
        return TransferType.FOUNDATION
