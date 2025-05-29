import random
from core.card import Card
from core.enums import Suit, Rank, Difficulty, TransferType
from core.difficulty import get_draw_amount

class Stock:
    def __init__(self):
        self._cards = []
        self._waste = []

        self.create_deck()
        self.shuffle_deck()

        self.drawn_waste_amount = 0

        self.initial_card_amount = 0

    def create_deck(self):
        self._cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self._waste.clear()
        self.initial_card_amount = len(self._cards)

    def shuffle_deck(self):
        random.shuffle(self._cards)

        def draw_cards(self, difficulty: Difficulty = Difficulty.HARD):
        if len(self._cards) == 0:
            self._cards = self._waste.copy()
            self._waste.clear()

        draw_amount = get_draw_amount(difficulty)
        drawn_cards = []

        for _ in range(draw_amount):
            if self._cards:
                drawn_cards.append(self._cards.pop())
            else:
                break

        self.drawn_waste_amount = 0
        self._waste.extend(drawn_cards)
        return drawn_cards
    
    def remove_card_from_waste(self, card: Card):
        if card in self._waste:
            self._waste.remove(card)
            return True
        return False
    
    def get_waste(self, difficulty: Difficulty = Difficulty.HARD):
        """
        Returns the visible cards in the waste pile based on difficulty.
        
        In easy mode: show 1 card (the top card)
        In hard mode: show up to 3 cards (the last 3 cards in waste)
        """
        if not self._waste:
            return []
        
        draw_amount = get_draw_amount(difficulty)
        available_cards = len(self._waste) - self.drawn_waste_amount
        visible_count = min(draw_amount, available_cards)
        
        if visible_count <= 0:
            return []
        
        # Return the last 'visible_count' cards from the remaining waste
        start_index = len(self._waste) - available_cards
        return self._waste[start_index:start_index + visible_count]
    
    def get_remaining_cards(self):
        return len(self._cards)
    
    def is_empty(self):
        return not self._cards and not self._waste
    
    def reset(self):
        self._cards = self._waste.copy()
        self._waste.clear()

    def remove_random_card(self):
        if self._cards:
            return self._cards.pop(random.randint(0, len(self._cards) - 1))
        return None

    def get_type():
        return TransferType.STOCK
    
    def is_waste_empty(self):
        return not self._waste

    def draw_first_card_from_waste(self, difficulty = Difficulty.HARD) -> Card:
        """
        Removes and returns the first available card from the waste pile.
        This is used when a card is transferred from the waste to another pile.
        """
        available_cards = len(self._waste) - self.drawn_waste_amount
        if available_cards <= 0:
            return None
        
        if self._waste:
            # Remove the topmost available card (which is at the end minus drawn_waste_amount)
            card_index = len(self._waste) - self.drawn_waste_amount - 1
            card = self._waste.pop(card_index)
            return card
        return None
    
    def can_draw_from_waste(self, difficulty: Difficulty = Difficulty.HARD) -> bool:
        """
        Checks if there are cards available to draw from the waste pile.
        """
        available_cards = len(self._waste) - self.drawn_waste_amount
        return available_cards > 0
    
    def can_draw(self) -> bool:
        return len(self._cards) > 0
    
    def get_card_percent(self) -> float:
        total_cards = self.initial_card_amount
        if total_cards == 0:
            return 0.0
        return (len(self._cards) + len(self._waste)) / total_cards
    
    def copy(self) -> 'Stock':
        new_stock = Stock()
        new_stock._cards = self._cards.copy()
        new_stock._waste = self._waste.copy()
        new_stock.drawn_waste_amount = self.drawn_waste_amount
        return new_stock
