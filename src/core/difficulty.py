"""
Funkcje pomocnicze związane z poziomem trudności gry.
"""

from core.enums import Difficulty
    
def get_draw_amount(difficulty: Difficulty) -> int:
    """
    Zwraca liczbę kart do dobierania w zależności od poziomu trudności.
    
    Args:
        difficulty (Difficulty): Poziom trudności gry
        
    Returns:
        int: 3 dla trudnego poziomu, 1 dla łatwego
    """
    return 3 if difficulty == Difficulty.HARD else 1
