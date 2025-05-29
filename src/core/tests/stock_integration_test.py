"""
Integration test for stock logic to verify the fixes work in a real game scenario.
This test verifies that the stock logic correctly handles drawing cards, 
managing waste, and transferring cards in an actual game context.
"""
import pytest
from core.game import SolitareGame
from core.enums import Difficulty
from core.transfer import StockTransfer, TableauTransfer

def mock_transfer_listener(time_enum):
    """Mock transfer listener for testing"""
    pass

def test_stock_integration_easy_mode():
    """Test stock functionality in easy mode (draw 1 card)"""
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    # Game setup draws cards during initialization, so let's clear and start fresh
    initial_waste_count = len(game.stock._waste)
    
    # Draw cards from stock in easy mode
    drawn = game.stock.draw_cards(Difficulty.EASY)
    assert len(drawn) == 1, "Should draw 1 card in easy mode"
    
    # Verify waste has the previously drawn cards plus the new one
    assert len(game.stock._waste) == initial_waste_count + 1
    assert game.stock.get_top_waste_card() == drawn[0]
    
    # Verify visible waste shows only 1 card in easy mode
    visible_waste = game.stock.get_waste(Difficulty.EASY)
    assert len(visible_waste) == 1
    assert visible_waste[0] == drawn[0]

def test_stock_integration_hard_mode():
    """Test stock functionality in hard mode (draw 3 cards)"""
    game = SolitareGame(Difficulty.HARD, transfer_listener=mock_transfer_listener)
    
    # Game setup draws cards during initialization, so track the initial state
    initial_waste_count = len(game.stock._waste)
    
    # Draw cards from stock in hard mode
    drawn = game.stock.draw_cards(Difficulty.HARD)
    assert len(drawn) == 3, "Should draw 3 cards in hard mode"
    
    # Verify waste has the previously drawn cards plus the new ones
    assert len(game.stock._waste) == initial_waste_count + 3
    assert game.stock.get_top_waste_card() == drawn[-1]  # Last card drawn is on top
    
    # Verify visible waste shows up to 3 cards in hard mode
    visible_waste = game.stock.get_waste(Difficulty.HARD)
    # Should show the last 3 cards (which are the ones we just drew)
    assert len(visible_waste) == 3
    assert visible_waste == game.stock._waste[-3:]

def test_stock_transfer_integration():
    """Test that StockTransfer works correctly with the new stock logic"""
    game = SolitareGame(Difficulty.HARD, transfer_listener=mock_transfer_listener)
    
    # Draw cards to create waste
    game.stock.draw_cards(Difficulty.HARD)
    
    # Create a stock transfer
    stock_transfer = StockTransfer(game.stock, Difficulty.HARD)
    
    # Check if we can create an offer
    assert stock_transfer.stock.can_draw_from_waste()
    
    offer = stock_transfer.create_offer(None)
    assert offer is not None
    assert offer.item is not None
    
    # The offered card should be the top waste card
    top_card = game.stock.get_top_waste_card()
    assert offer.item == top_card
    
    # Complete the offer
    initial_waste_count = len(game.stock._waste)
    offer.complete()
    
    # Verify the card was removed from waste
    assert len(game.stock._waste) == initial_waste_count - 1
    assert top_card not in game.stock._waste

def test_stock_recycle_integration():
    """Test that stock properly recycles waste when stock is empty"""
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    # Draw all cards from stock
    total_cards_drawn = 0
    while game.stock._cards:
        drawn = game.stock.draw_cards(Difficulty.EASY)
        total_cards_drawn += len(drawn)
    
    # Verify stock is empty but waste has cards
    assert len(game.stock._cards) == 0
    waste_count = len(game.stock._waste)
    assert waste_count > 0
    
    # Draw again - should trigger recycling
    drawn = game.stock.draw_cards(Difficulty.EASY)
    
    # Verify recycling worked
    assert len(drawn) == 1
    assert len(game.stock._waste) == 1  # Only the newly drawn card
    assert len(game.stock._cards) == waste_count - 1  # Remaining recycled cards

def test_stock_empty_scenario():
    """Test behavior when stock and waste are both empty"""
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    # Exhaust all cards by drawing and removing them
    while game.stock._cards or game.stock._waste:
        if game.stock._cards:
            game.stock.draw_cards(Difficulty.EASY)
        if game.stock._waste:
            game.stock.draw_top_card_from_waste()
    
    # Verify everything is empty
    assert game.stock.is_empty()
    assert not game.stock.can_draw_from_waste()
    assert game.stock.get_top_waste_card() is None
    
    # Try to draw from empty stock
    drawn = game.stock.draw_cards(Difficulty.EASY)
    assert len(drawn) == 0
    
    # Stock transfer should not be able to create offers
    stock_transfer = StockTransfer(game.stock, Difficulty.EASY)
    offer = stock_transfer.create_offer(None)
    assert offer is None

def test_stock_with_multiple_difficulties():
    """Test that stock works correctly when switching between difficulties"""
    game = SolitareGame(Difficulty.HARD, transfer_listener=mock_transfer_listener)
    
    # Game initialization draws 3 cards, so we have initial waste
    initial_waste_count = len(game.stock._waste)
    assert initial_waste_count == 3  # Should be 3 from initialization
    
    # Draw 3 cards in hard mode
    drawn_hard = game.stock.draw_cards(Difficulty.HARD)
    assert len(drawn_hard) == 3
    
    # View waste in easy mode (should show only 1 card)
    waste_easy = game.stock.get_waste(Difficulty.EASY)
    assert len(waste_easy) == 1
    assert waste_easy[0] == drawn_hard[-1]  # Should be the top card
    
    # View waste in hard mode (should show all 3 cards)
    waste_hard = game.stock.get_waste(Difficulty.HARD)
    assert len(waste_hard) == 3
    assert waste_hard == drawn_hard
    
    # Draw 1 more card in easy mode
    drawn_easy = game.stock.draw_cards(Difficulty.EASY)
    assert len(drawn_easy) == 1
    
    # Total waste should now have initial + 3 + 1 = 7 cards
    assert len(game.stock._waste) == initial_waste_count + 3 + 1
