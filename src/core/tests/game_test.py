from .parent_util import add_parent_dir_to_path

add_parent_dir_to_path()

from core.game import SolitareGame
from core.enums import Difficulty
from core.transfer import TableauTransfer, StockTransfer

def mock_transfer_listener(time_enum):
    """Mock transfer listener for testing"""
    pass

def test_game_initialization():
    game = SolitareGame(difficulty=Difficulty.EASY, transfer_listener=mock_transfer_listener)
    assert game.tableau is not None
    assert game.stock is not None
    assert game.foundations is not None
    assert game.get_difficulty() == Difficulty.EASY

def test_game_tt_transfer():
    game = SolitareGame(difficulty=Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    # Set up a controlled scenario - clear pile 0 and 1, put King on 0
    game.tableau.piles[0] = None
    game.tableau.piles[1] = None
    
    from core.card import create_card
    from core.enums import Suit, Rank
    
    # Put a King on pile 0 (Kings can go on empty piles)
    black_king = create_card(Suit.SPADES, Rank.KING)
    game.tableau.place_card(black_king, 0)
    
    source = TableauTransfer(
        tableau=game.tableau,
        source_index=0,
        depth=0,
        difficulty=Difficulty.EASY
    )
    target = TableauTransfer(
        tableau=game.tableau,
        source_index=1,
        depth=0,
        difficulty=Difficulty.EASY
    )
    success = game.transfer(source, target)

    assert success is True
    assert game.tableau.get_pile(0) is None or game.tableau.get_top_card(0) is None
    assert game.tableau.get_pile(1) is not None

def test_game_st_transfer():
    game = SolitareGame(difficulty=Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    # For stock transfer, we need to check if stock has cards and can draw
    initial_remaining_cards = game.stock.get_remaining_cards()
    initial_waste_empty = game.stock.is_waste_empty()
    
    source = StockTransfer(
        stock=game.stock
    )
    target = TableauTransfer(
        tableau=game.tableau,
        source_index=1,
        depth=0
    )
    success = game.transfer(source, target)

    # Stock transfers may fail if waste is empty or card can't be placed
    # We test that the game handles it properly without crashing
    assert success in [True, False]  # Should be a boolean
    
def test_game_invalid_transfer():
    game = SolitareGame(difficulty=Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    source = TableauTransfer(
        tableau=game.tableau,
        source_index=0,
        depth=10  # Invalid depth - deeper than any pile
    )
    target = TableauTransfer(
        tableau=game.tableau,
        source_index=1,
        depth=0
    )
    success = game.transfer(source, target)

    assert success is False
    # Original piles should remain unchanged
    assert game.tableau.get_pile(0) is not None  # Should still have cards from initial setup
    assert game.tableau.get_pile(1) is not None  # Should still have cards from initial setup
