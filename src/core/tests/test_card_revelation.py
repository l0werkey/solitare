from .parent_util import add_parent_dir_to_path

add_parent_dir_to_path()

from core.tableau import Tableau
from core.pile_part import create_pile
from core.enums import Suit, Rank, Difficulty
from core.card import create_card
from core.game import SolitareGame
from core.transfer import TableauTransfer

def mock_transfer_listener(time_enum):
    """Mock transfer listener for testing"""
    pass

def test_card_revelation_on_remove_top_card():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING, hidden=True)  # This will be revealed
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN, hidden=False)  # This is visible and will be removed
    
    tableau.piles[0] = create_pile(king_hearts, queen_spades)
    
    assert king_hearts.hidden == True, "King should initially be hidden"
    assert queen_spades.hidden == False, "Queen should initially be visible"
    
    removed_card = tableau.remove_top_card(0)
    
    assert removed_card.rank == Rank.QUEEN, "Should have removed the Queen"
    
    assert king_hearts.hidden == False, "King should now be revealed after Queen was removed"
    
    top_card = tableau.get_top_card(0)
    assert top_card.rank == Rank.KING, "King should now be the top card"

def test_card_revelation_on_move_pile():
    tableau = Tableau()
    
    ace_hearts = create_card(Suit.HEARTS, Rank.ACE, hidden=True)  # This will be revealed
    king_spades = create_card(Suit.SPADES, Rank.KING, hidden=False)
    queen_hearts = create_card(Suit.HEARTS, Rank.QUEEN, hidden=False)
    
    tableau.piles[0] = create_pile(ace_hearts, king_spades, queen_hearts)
    
    assert ace_hearts.hidden == True, "Ace should initially be hidden"
    
    success = tableau.move_pile(0, 1, 1)
    assert success == True, "Move should succeed"
    
    assert ace_hearts.hidden == False, "Ace should now be revealed after cards were moved"
    top_card = tableau.get_top_card(0)
    assert top_card.rank == Rank.ACE, "Ace should now be the top card"

def test_no_revelation_when_card_already_visible():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING, hidden=False)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN, hidden=False)
    
    tableau.piles[0] = create_pile(king_hearts, queen_spades)
    
    tableau.remove_top_card(0)
    
    assert king_hearts.hidden == False, "King should remain visible"

def test_card_revelation_with_transfer_system():
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    game.tableau.piles = [None] * 7
    
    hidden_ace = create_card(Suit.HEARTS, Rank.ACE, hidden=True)  # This will be revealed
    visible_king = create_card(Suit.SPADES, Rank.KING, hidden=False)
    
    game.tableau.piles[0] = create_pile(hidden_ace, visible_king)
    
    assert hidden_ace.hidden == True, "Ace should initially be hidden"
    assert visible_king.hidden == False, "King should be visible"
    
    removed_card = game.tableau.remove_top_card(0)
    
    assert removed_card.rank == Rank.KING, "Should have removed the King"
    
    assert hidden_ace.hidden == False, "Ace should now be revealed after King was removed"
    
    top_card = game.tableau.get_top_card(0)
    assert top_card.rank == Rank.ACE, "Ace should now be the top card in source pile"

def test_card_revelation_with_single_card_transfer():
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    game.tableau.piles = [None] * 7
    
    hidden_jack = create_card(Suit.CLUBS, Rank.JACK, hidden=True)  # This will be revealed
    visible_ten = create_card(Suit.DIAMONDS, Rank.TEN, hidden=False)  # This will be moved
    
    game.tableau.piles[0] = create_pile(hidden_jack, visible_ten)
    
    target_jack = create_card(Suit.SPADES, Rank.JACK, hidden=False)
    game.tableau.piles[1] = create_pile(target_jack)
    
    assert hidden_jack.hidden == True, "Jack should initially be hidden"
    assert visible_ten.hidden == False, "Ten should be visible"
    
    success = game.tableau.move_pile(0, 1, 1)  # Move just the Ten (depth 1)
    assert success == True, "Move should succeed"
    
    assert hidden_jack.hidden == False, "Jack should now be revealed after Ten was moved"
    
    top_card = game.tableau.get_top_card(0)
    assert top_card.rank == Rank.JACK, "Jack should now be the top card in source pile"
    
    dest_top_card = game.tableau.get_top_card(1)
    assert dest_top_card.rank == Rank.TEN, "Ten should be the top card in destination pile"

def test_no_revelation_when_transferring_from_empty_pile():
    """Test that transfers from empty piles are handled gracefully."""
    game = SolitareGame(Difficulty.EASY, transfer_listener=mock_transfer_listener)
    
    game.tableau.piles[0] = None
    game.tableau.piles[1] = None
    
    source_transfer = TableauTransfer(
        tableau=game.tableau,
        source_index=0,  # Empty pile
        depth=0,
        difficulty=Difficulty.EASY
    )
    
    target_transfer = TableauTransfer(
        tableau=game.tableau,
        source_index=1,
        depth=0,
        difficulty=Difficulty.EASY
    )
    
    transfer_success = game.transfer(source_transfer, target_transfer)
    assert transfer_success == False, "Transfer from empty pile should fail"
