from .parent_util import add_parent_dir_to_path

add_parent_dir_to_path()

from core.tableau import Tableau
from core.pile_part import create_pile
from core.enums import Suit, Rank, Color
from core.card import create_card

def test_tableau_initialization():
    tableau = Tableau()
    assert len(tableau.piles) == 7, "Tableau should have 7 piles"
    for i in range(7):
        assert tableau.piles[i] is None, f"Pile {i} should be empty on initialization"

def test_can_place_card_on_empty_pile():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    ace_clubs = create_card(Suit.CLUBS, Rank.ACE)
    
    assert tableau.can_place_card(king_hearts, 0) == True, "Should be able to place King on empty pile"
    assert tableau.can_place_card(queen_spades, 0) == False, "Should not be able to place Queen on empty pile"
    assert tableau.can_place_card(ace_clubs, 0) == False, "Should not be able to place Ace on empty pile"

def test_can_place_card_on_existing_pile():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    tableau.piles[0] = create_pile(king_hearts)
    
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    queen_hearts = create_card(Suit.HEARTS, Rank.QUEEN)
    jack_clubs = create_card(Suit.CLUBS, Rank.JACK)
    king_spades = create_card(Suit.SPADES, Rank.KING)
    
    assert tableau.can_place_card(queen_spades, 0) == True, "Should be able to place black Queen on red King"
    assert tableau.can_place_card(queen_hearts, 0) == False, "Should not be able to place red Queen on red King"
    assert tableau.can_place_card(jack_clubs, 0) == False, "Should not be able to place Jack on King (wrong rank)"
    assert tableau.can_place_card(king_spades, 0) == False, "Should not be able to place King on King (same rank)"

def test_place_card_single():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    
    assert tableau.place_card(king_hearts, 0) == True, "Should successfully place King"
    assert tableau.get_top_card(0).rank == Rank.KING, "Top card should be King"
    assert tableau.get_pile_size(0) == 1, "Pile should have 1 card"
    
    assert tableau.place_card(queen_spades, 0) == True, "Should successfully place Queen"
    assert tableau.get_top_card(0).rank == Rank.QUEEN, "Top card should be Queen"
    assert tableau.get_pile_size(0) == 2, "Pile should have 2 cards"

def test_place_card_invalid():
    tableau = Tableau()
    
    queen_hearts = create_card(Suit.HEARTS, Rank.QUEEN)
    
    assert tableau.place_card(queen_hearts, 0) == False, "Should reject non-King on empty pile"
    assert tableau.is_pile_empty(0) == True, "Pile should remain empty"

def test_remove_top_card():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    tableau.piles[0] = create_pile(king_hearts, queen_spades)
    
    removed_card = tableau.remove_top_card(0)
    assert removed_card.rank == Rank.QUEEN, "Should remove Queen"
    assert tableau.get_top_card(0).rank == Rank.KING, "King should now be on top"
    assert tableau.get_pile_size(0) == 1, "Pile should have 1 card left"
    
    removed_card = tableau.remove_top_card(0)
    assert removed_card.rank == Rank.KING, "Should remove King"
    assert tableau.is_pile_empty(0) == True, "Pile should be empty"

def test_remove_top_card_empty_pile():
    tableau = Tableau()
    
    removed_card = tableau.remove_top_card(0)
    assert removed_card is None, "Should return None when removing from empty pile"

def test_can_move_sequence_valid():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    jack_hearts = create_card(Suit.HEARTS, Rank.JACK)
    tableau.piles[0] = create_pile(king_hearts, queen_spades, jack_hearts)
    
    assert tableau.can_move_sequence(0, 0) == True, "Should be able to move entire valid sequence"
    assert tableau.can_move_sequence(0, 1) == True, "Should be able to move Queen-Jack sequence"
    assert tableau.can_move_sequence(0, 2) == True, "Should be able to move single Jack"

def test_can_move_sequence_invalid():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_hearts = create_card(Suit.HEARTS, Rank.QUEEN)
    tableau.piles[0] = create_pile(king_hearts, queen_hearts)
    
    assert tableau.can_move_sequence(0, 0) == False, "Should not be able to move invalid sequence"

def test_move_pile_king_to_empty():
    tableau = Tableau()
    
    king_spades = create_card(Suit.SPADES, Rank.KING)
    queen_hearts = create_card(Suit.HEARTS, Rank.QUEEN)
    tableau.piles[0] = create_pile(king_spades, queen_hearts)
    
    assert tableau.move_pile(0, 1, 0) == True, "Should successfully move King to empty pile"
    assert tableau.is_pile_empty(0) == True, "Source pile should be empty"
    assert tableau.get_top_card(1).rank == Rank.QUEEN, "Target pile should have Queen on top"
    assert tableau.get_pile_size(1) == 2, "Target pile should have 2 cards"

def test_move_pile_sequence():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    jack_hearts = create_card(Suit.HEARTS, Rank.JACK)
    tableau.piles[0] = create_pile(king_hearts, queen_spades, jack_hearts)
    ace_spades = create_card(Suit.SPADES, Rank.ACE)
    tableau.piles[1] = create_pile(ace_spades)
    
    assert tableau.move_pile(0, 1, 1) == False, "Should not be able to place Queen on Ace"
    
    queen_clubs = create_card(Suit.CLUBS, Rank.QUEEN)
    tableau.piles[1] = create_pile(queen_clubs)
    
    assert tableau.move_pile(0, 1, 2) == True, "Should be able to place Jack on Queen"
    assert tableau.get_top_card(0).rank == Rank.QUEEN, "Source should have Queen on top"
    assert tableau.get_top_card(1).rank == Rank.JACK, "Target should have Jack on top"

def test_move_pile_invalid_cases():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    tableau.piles[0] = create_pile(king_hearts)
    
    assert tableau.move_pile(-1, 1, 0) == False, "Should reject negative source index"
    assert tableau.move_pile(0, 7, 0) == False, "Should reject out-of-bounds target index"
    assert tableau.move_pile(0, 0, 0) == False, "Should reject same source and target"
    
    assert tableau.move_pile(1, 0, 0) == False, "Should reject moving from empty pile"
    
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    tableau.piles[0] = create_pile(queen_spades)
    assert tableau.move_pile(0, 1, 0) == False, "Should reject placing non-King on empty pile"

def test_get_top_card():
    tableau = Tableau()
    
    assert tableau.get_top_card(0) is None, "Should return None for empty pile"
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    tableau.piles[0] = create_pile(king_hearts, queen_spades)
    
    top_card = tableau.get_top_card(0)
    assert top_card.rank == Rank.QUEEN, "Should return Queen as top card"
    assert top_card.suit == Suit.SPADES, "Top card should be Spades"

def test_is_pile_empty():
    tableau = Tableau()
    
    for i in range(7):
        assert tableau.is_pile_empty(i) == True, f"Pile {i} should be empty initially"
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    tableau.piles[0] = create_pile(king_hearts)
    
    assert tableau.is_pile_empty(0) == False, "Pile 0 should not be empty"
    assert tableau.is_pile_empty(1) == True, "Pile 1 should still be empty"

def test_get_pile_size():
    tableau = Tableau()
    
    assert tableau.get_pile_size(0) == 0, "Empty pile should have size 0"
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    tableau.piles[0] = create_pile(king_hearts)
    assert tableau.get_pile_size(0) == 1, "Pile should have size 1"
    
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    jack_hearts = create_card(Suit.HEARTS, Rank.JACK)
    tableau.piles[0] = create_pile(king_hearts, queen_spades, jack_hearts)
    assert tableau.get_pile_size(0) == 3, "Pile should have size 3"

def test_boundary_conditions():
    tableau = Tableau()
    
    assert tableau.can_place_card(create_card(Suit.HEARTS, Rank.KING), -1) == False
    assert tableau.can_place_card(create_card(Suit.HEARTS, Rank.KING), 7) == False
    assert tableau.get_top_card(-1) is None
    assert tableau.get_top_card(7) is None
    assert tableau.remove_top_card(-1) is None
    assert tableau.remove_top_card(7) is None
    assert tableau.is_pile_empty(-1) == False
    assert tableau.is_pile_empty(7) == False
    assert tableau.get_pile_size(-1) == 0
    assert tableau.get_pile_size(7) == 0

def test_complex_tableau_scenario():
    tableau = Tableau()
    
    king_hearts = create_card(Suit.HEARTS, Rank.KING)
    queen_spades = create_card(Suit.SPADES, Rank.QUEEN)
    jack_hearts = create_card(Suit.HEARTS, Rank.JACK)
    tableau.piles[0] = create_pile(king_hearts, queen_spades, jack_hearts)
    
    queen_clubs = create_card(Suit.CLUBS, Rank.QUEEN)
    tableau.piles[1] = create_pile(queen_clubs)
    
    assert tableau.move_pile(0, 1, 2) == True, "Should move Jack to Queen"
    assert tableau.get_top_card(0).rank == Rank.QUEEN, "Pile 0 should have Queen on top"
    assert tableau.get_top_card(1).rank == Rank.JACK, "Pile 1 should have Jack on top"
    assert tableau.get_pile_size(1) == 2, "Pile 1 should have 2 cards"
    
    assert tableau.move_pile(0, 2, 0) == True, "Should move King-Queen to empty pile"
    assert tableau.is_pile_empty(0) == True, "Pile 0 should be empty"
    assert tableau.get_top_card(2).rank == Rank.QUEEN, "Pile 2 should have Queen on top"
    assert tableau.get_pile_size(2) == 2, "Pile 2 should have 2 cards"
