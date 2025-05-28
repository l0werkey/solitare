from .parent_util import add_parent_dir_to_path

add_parent_dir_to_path()

from core.foundations import Foundation, Foundations
from core.pile_part import create_pile
from core.enums import Suit, Rank, Color
from core.card import create_card

def test_foundation_can_place_card():
    foundation = Foundation(Suit.HEARTS)
    card1 = create_card(Suit.HEARTS, Rank.ACE)
    card2 = create_card(Suit.HEARTS, Rank.TWO)
    card3 = create_card(Suit.DIAMONDS, Rank.ACE)

    assert foundation.can_place_card(card1) == True, "Foundation should accept Ace of Hearts"
    assert foundation.can_place_card(card2) == False, "Foundation should not accept Two of Hearts"
    assert foundation.can_place_card(card3) == False, "Foundation should not accept Ace of Diamonds"

def test_foundation_with_pile():
    foundation = Foundation(Suit.HEARTS)
    foundation.pile = create_pile(create_card(Suit.HEARTS, Rank.ACE))

    card1 = create_card(Suit.HEARTS, Rank.TWO)
    card2 = create_card(Suit.HEARTS, Rank.THREE)
    card3 = create_card(Suit.HEARTS, Rank.FOUR)

    assert foundation.can_place_card(card1) == True, "Foundation should accept Two of Hearts"
    assert foundation.can_place_card(card2) == False, "Foundation should not accept Three of Hearts"
    assert foundation.can_place_card(card3) == False, "Foundation should not accept Four of Hearts"

def test_foundation_finished():
    foundation = Foundation(Suit.HEARTS)
    foundation.pile = create_pile(*[create_card(Suit.HEARTS, rank) for rank in Rank])
    assert foundation.is_finished() == True, "Foundation should be finished with all cards"

def test_foundations_can_place_card():
    foundations = Foundations()
    card1 = create_card(Suit.HEARTS, Rank.ACE)
    card2 = create_card(Suit.HEARTS, Rank.TWO)
    card3 = create_card(Suit.DIAMONDS, Rank.ACE)

    assert foundations.can_place_card(card1) == True, "Foundations should accept Ace of Hearts"
    assert foundations.can_place_card(card2) == False, "Foundations should not accept Two of Hearts"
    assert foundations.can_place_card(card3) == True, "Foundations should accept Ace of Diamonds"

def test_foundations_attempt_place_card():
    foundations = Foundations()
    card1 = create_card(Suit.HEARTS, Rank.ACE)
    card2 = create_card(Suit.HEARTS, Rank.TWO)
    card3 = create_card(Suit.DIAMONDS, Rank.ACE)

    assert foundations.attempt_place_card(card1) == True, "Foundations should accept Ace of Hearts"
    assert foundations.attempt_place_card(card2) == True, "Foundations should accept Two of Hearts"
    assert foundations.attempt_place_card(card3) == True, "Foundations should accept Ace of Diamonds"
    assert foundations.foundations[Suit.HEARTS].pile.get_last().get_card().rank == Rank.TWO, "Foundation should have Two of Hearts on top"
    assert foundations.foundations[Suit.DIAMONDS].pile.get_last().get_card().rank == Rank.ACE, "Foundation should have Ace of Diamonds on top"
