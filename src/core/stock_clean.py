# filepath: c:\Users\rogal\Desktop\Dev\pasjans\src\core\stock.py
import random
from core.card import Card
from core.enums import Suit, Rank, Difficulty, TransferType
from core.difficulty import get_draw_amount

class Stock:
    def __init__(self):
        self._cards = []
        self._waste = []
        self.initial_card_amount = 0
        self.create_deck()
        self.shuffle_deck()

    def create_deck(self):
        self._cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self._waste.clear()
        self.initial_card_amount = len(self._cards)

    def shuffle_deck(self):
        random.shuffle(self._cards)

    def draw_cards(self, difficulty: Difficulty = Difficulty.HARD):
        """
        Draws cards from the stock pile to the waste pile.
        If stock is empty, moves all waste cards back to stock.
        """
        if len(self._cards) == 0:
            if self._waste:
                self._cards = self._waste.copy()
                self._waste.clear()
            else:
                return []

        draw_amount = get_draw_amount(difficulty)
        drawn_cards = []

        for _ in range(draw_amount):
            if self._cards:
                drawn_cards.append(self._cards.pop())
            else:
                break

        self._waste.extend(drawn_cards)
        return drawn_cards
    
    def remove_card_from_waste(self, card: Card):
        """
        Removes a specific card from the waste pile.
        Used when a card is moved to foundations or tableau.
        """
        if card in self._waste:
            self._waste.remove(card)
            return True
        return False
    
    def get_waste(self, difficulty: Difficulty = Difficulty.HARD):
        """
        Returns the visible cards in the waste pile based on difficulty.
        
        In easy mode (draw 1): show only the last card
        In hard mode (draw 3): show up to the last 3 cards
        """
        if not self._waste:
            return []
        
        draw_amount = get_draw_amount(difficulty)
        # Show the last 'draw_amount' cards, or all cards if fewer exist
        return self._waste[-draw_amount:] if len(self._waste) >= draw_amount else self._waste.copy()
    
    def get_top_waste_card(self):
        """Returns the topmost (playable) card from waste, or None if waste is empty"""
        return self._waste[-1] if self._waste else None
    
    def get_remaining_cards(self):
        return len(self._cards)
    
    def is_empty(self):
        return not self._cards and not self._waste
    
    def reset(self):
        """Reset all waste cards back to stock pile"""
        self._cards = self._waste.copy()
        self._waste.clear()

    def remove_random_card(self):
        """Remove a random card from stock (used during game setup)"""
        if self._cards:
            return self._cards.pop(random.randint(0, len(self._cards) - 1))
        return None

    def get_type():
        return TransferType.STOCK
    
    def is_waste_empty(self):
        return not self._waste

    def draw_top_card_from_waste(self) -> Card:
        """
        Removes and returns the topmost card from the waste pile.
        This is the card that would be played when moving from stock.
        """
        if self._waste:
            return self._waste.pop()
        return None
    
    def can_draw_from_waste(self, difficulty: Difficulty = Difficulty.HARD) -> bool:
        """
        Checks if there are cards available to draw from the waste pile.
        """
        return len(self._waste) > 0
    
    def can_draw(self) -> bool:
        """Check if we can draw cards from the stock pile"""
        return len(self._cards) > 0 or len(self._waste) > 0
    
    def get_card_percent(self) -> float:
        total_cards = self.initial_card_amount
        if total_cards == 0:
            return 0.0
        return (len(self._cards) + len(self._waste)) / total_cards
    
    def copy(self) -> 'Stock':
        new_stock = Stock()
        new_stock._cards = self._cards.copy()
        new_stock._waste = self._waste.copy()
        new_stock.initial_card_amount = self.initial_card_amount
        return new_stock
