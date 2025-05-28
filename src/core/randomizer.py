"""
Funkcje pomocnicze do generowania losowych wartości dla kart.
"""

from core.enums import Suit, Rank, Color
import random

def get_random_from_enum(enum_cls):
    """
    Zwraca losowy element z podanej enumeracji.
    
    Args:
        enum_cls: Klasa enumeracji do wyboru
        
    Returns:
        Losowy element z enumeracji
    """
    return random.choice(list(enum_cls))

# Funkcje lambda dla wygody użycia
get_random_suit = lambda: get_random_from_enum(Suit)  # Losowy kolor karty
get_random_rank = lambda: get_random_from_enum(Rank)  # Losowa ranga karty