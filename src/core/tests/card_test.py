from .parent_util import add_parent_dir_to_path

add_parent_dir_to_path()

from core.card import create_card
from core.enums import Suit, Rank

def test_rank_comparison():
    card1 = create_card(rank=Rank.EIGHT)
    card2 = create_card(rank=Rank.SEVEN)
    assert card1.is_rank_higher(card2) == True, "Expected card1 to be higher than card2"
    assert card2.is_rank_higher(card1) == False, "Expected card2 to be lower than card1"

def test_suit_comparison():
    card1 = create_card(suit=Suit.HEARTS)
    card2 = create_card(suit=Suit.HEARTS)
    assert card1.is_same_suit(card2) == True, "Expected card1 and card2 to have the same suit"
    assert card2.is_same_suit(card1) == True, "Expected card2 and card1 to have the same suit"

def test_color_comparison():
    card1 = create_card(suit=Suit.HEARTS)
    card2 = create_card(suit=Suit.DIAMONDS)
    assert card1.is_same_color(card2) == True, "Expected card1 and card2 to have the same color"
    assert card2.is_same_color(card1) == True, "Expected card2 and card1 to have the same color"

def test_str_representation():
    card = create_card(Suit.HEARTS, Rank.EIGHT)
    assert str(card) == "EIGHT of HEARTS (RED)", "Expected string representation to match"

def test_clone():
    card = create_card()
    cloned_card = card.clone()
    assert cloned_card.suit == card.suit, "Expected cloned card to have the same suit"
    assert cloned_card.rank == card.rank, "Expected cloned card to have the same rank"
    # Weryfikacja czy klon jest innym obiektem
    assert cloned_card is not card, "Expected cloned card to be a different object"
