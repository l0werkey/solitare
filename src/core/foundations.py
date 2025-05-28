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
        
        return self.pile.get_last().get_card().rank == Rank.KING and self.pile.count() == len(Rank)
    
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

    def remove_top_card(self, suit):
        foundation = self.foundations.get(suit)
        if foundation is None or foundation.pile is None:
            return None
        
        pile = foundation.pile
        
        if pile.next is None:
            card = pile.get_card()
            foundation.pile = None
            return card
        
        current = pile
        while current.next.next is not None:
            current = current.next
        
        top_card = current.next.get_card()
        current.next = None
                
        return top_card

    def get_top_card(self, suit):
        foundation = self.foundations.get(suit)
        if foundation is None or foundation.pile is None:
            return None
        return foundation.pile.get_last().get_card()

    def copy_all(self):
        new_foundations = Foundations()
        for suit, foundation in self.foundations.items():
            new_foundations.foundations[suit] = foundation.copy()
        return new_foundations

    def get_all(self):
        return list(self.foundations.values())

    def get_type(self):
        return TransferType.FOUNDATION
    
    def place_card(self, card):
        if self.can_place_card(card):
            self.attempt_place_card(card)
            return True
        return False
