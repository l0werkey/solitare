import pytest
import sys
import os

# Przed zainporowaniem card musimy dodać katalog nadrzędny do sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from card import Card
from enums import Suit, Rank, Color

def test_rank_comparison():
    card1 = Card(Suit.HEARTS, Rank.EIGHT, Color.RED)
    card2 = Card(Suit.SPADES, Rank.SEVEN, Color.BLACK)
    assert card1.is_rank_higher(card2) == True
    assert card2.is_rank_higher(card1) == False

def test_suit_comparison():
    card1 = Card(Suit.HEARTS, Rank.EIGHT, Color.RED)
    card2 = Card(Suit.HEARTS, Rank.SEVEN, Color.BLACK)
    assert card1.is_same_suit(card2) == True
    assert card2.is_same_suit(card1) == True

def test_color_comparison():
    card1 = Card(Suit.HEARTS, Rank.EIGHT, Color.RED)
    card2 = Card(Suit.SPADES, Rank.SEVEN, Color.RED)
    assert card1.is_same_color(card2) == True
    assert card2.is_same_color(card1) == True