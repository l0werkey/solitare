# filepath: c:\Users\rogal\Desktop\Dev\pasjans\src\core\tests\stock_test.py
import pytest
from core.stock import Stock
from core.enums import Difficulty, Suit, Rank
from core.card import Card

class TestStock:
    def test_stock_initialization(self):
        """Test stock initialization creates a full deck"""
        stock = Stock()
        assert len(stock._cards) == 52
        assert len(stock._waste) == 0
        assert stock.initial_card_amount == 52

    def test_draw_cards_easy_difficulty(self):
        """Test drawing one card in easy mode"""
        stock = Stock()
        initial_count = len(stock._cards)
        
        drawn = stock.draw_cards(Difficulty.EASY)
        
        assert len(drawn) == 1
        assert len(stock._cards) == initial_count - 1
        assert len(stock._waste) == 1
        assert drawn[0] in stock._waste

    def test_draw_cards_hard_difficulty(self):
        """Test drawing three cards in hard mode"""
        stock = Stock()
        initial_count = len(stock._cards)
        
        drawn = stock.draw_cards(Difficulty.HARD)
        
        assert len(drawn) == 3
        assert len(stock._cards) == initial_count - 3
        assert len(stock._waste) == 3
        for card in drawn:
            assert card in stock._waste

    def test_get_waste_easy(self):
        """Test getting waste in easy mode shows only top card"""
        stock = Stock()
        
        # Draw some cards
        stock.draw_cards(Difficulty.HARD)  # Draw 3 cards
        
        waste = stock.get_waste(Difficulty.EASY)
        assert len(waste) == 1
        assert waste[0] == stock._waste[-1]  # Should be the last card

    def test_get_waste_hard(self):
        """Test getting waste in hard mode shows up to 3 cards"""
        stock = Stock()
        
        # Draw some cards
        stock.draw_cards(Difficulty.HARD)  # Draw 3 cards
        
        waste = stock.get_waste(Difficulty.HARD)
        assert len(waste) == 3
        assert waste == stock._waste[-3:]  # Should be the last 3 cards

    def test_get_top_waste_card(self):
        """Test getting the top waste card"""
        stock = Stock()
        
        # Initially no waste cards
        assert stock.get_top_waste_card() is None
        
        # Draw cards
        drawn = stock.draw_cards(Difficulty.HARD)
        top_card = stock.get_top_waste_card()
        
        assert top_card is not None
        assert top_card == drawn[-1]  # Should be the last card drawn

    def test_draw_top_card_from_waste(self):
        """Test drawing the top card from waste"""
        stock = Stock()
        
        # Draw cards to waste
        drawn = stock.draw_cards(Difficulty.HARD)
        initial_waste_count = len(stock._waste)
        expected_card = stock._waste[-1]
        
        # Draw top card from waste
        card = stock.draw_top_card_from_waste()
        
        assert card == expected_card
        assert len(stock._waste) == initial_waste_count - 1
        assert card not in stock._waste

    def test_can_draw_from_waste(self):
        """Test checking if we can draw from waste"""
        stock = Stock()
        
        # Initially no waste cards
        assert not stock.can_draw_from_waste()
        
        # Draw cards to waste
        stock.draw_cards(Difficulty.HARD)
        assert stock.can_draw_from_waste()
        
        # Remove all waste cards
        while stock._waste:
            stock.draw_top_card_from_waste()
        
        assert not stock.can_draw_from_waste()

    def test_stock_recycle_when_empty(self):
        """Test that stock recycles waste when stock is empty"""
        stock = Stock()
        
        # Draw all cards from stock to waste
        while stock._cards:
            stock.draw_cards(Difficulty.HARD)
        
        # Verify stock is empty and waste has cards
        assert len(stock._cards) == 0
        waste_count = len(stock._waste)
        assert waste_count > 0
        
        # Try to draw again - should recycle waste to stock
        drawn = stock.draw_cards(Difficulty.HARD)
        
        assert len(drawn) > 0
        assert len(stock._waste) == len(drawn)  # Only the newly drawn cards
        assert len(stock._cards) == waste_count - len(drawn)  # Remaining recycled cards

    def test_remove_card_from_waste(self):
        """Test removing a specific card from waste"""
        stock = Stock()
        
        # Draw cards
        drawn = stock.draw_cards(Difficulty.HARD)
        card_to_remove = drawn[1]  # Middle card
        initial_waste_count = len(stock._waste)
        
        # Remove the card
        result = stock.remove_card_from_waste(card_to_remove)
        
        assert result is True
        assert len(stock._waste) == initial_waste_count - 1
        assert card_to_remove not in stock._waste
        
        # Try to remove a card that's not in waste
        dummy_card = Card(Suit.HEARTS, Rank.ACE)
        result = stock.remove_card_from_waste(dummy_card)
        assert result is False

    def test_reset(self):
        """Test resetting waste cards back to stock"""
        stock = Stock()
        
        # Draw some cards to waste
        stock.draw_cards(Difficulty.HARD)
        waste_count = len(stock._waste)
        stock_count = len(stock._cards)
        
        # Reset
        stock.reset()
        
        assert len(stock._cards) == waste_count
        assert len(stock._waste) == 0

    def test_is_empty(self):
        """Test checking if stock is completely empty"""
        stock = Stock()
        
        # Initially not empty (has cards in stock)
        assert not stock.is_empty()
        
        # Draw some cards to create waste
        stock.draw_cards(Difficulty.HARD)
        
        # Remove all cards from stock
        stock._cards.clear()
        assert not stock.is_empty()  # Still has waste
        
        # Remove all waste cards too
        stock._waste.clear()
        assert stock.is_empty()  # Now truly empty

    def test_copy(self):
        """Test copying a stock"""
        stock = Stock()
        stock.draw_cards(Difficulty.HARD)
        
        copied_stock = stock.copy()
        
        assert len(copied_stock._cards) == len(stock._cards)
        assert len(copied_stock._waste) == len(stock._waste)
        assert copied_stock.initial_card_amount == stock.initial_card_amount
        
        # Verify it's a real copy (modifying one doesn't affect the other)
        stock.draw_cards(Difficulty.EASY)
        assert len(copied_stock._cards) != len(stock._cards)
