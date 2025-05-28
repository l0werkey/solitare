"""
Definicja klasy Card reprezentującej kartę do gry oraz funkcji pomocniczych.
Zawiera logikę porównywania kart i operacji na nich.
"""

from core.enums import Suit, Rank, Color
from core.randomizer import get_random_suit, get_random_rank

class Card:
    """
    Reprezentuje pojedynczą kartę do gry.
    
    Zawiera informacje o kolorze, randze i czy karta jest ukryta.
    Udostępnia metody do porównywania kart i operacji na nich.
    """
    
    def __init__(self, suit: Suit, rank: Rank, hidden: bool = False):
        """
        Inicjalizuje nową kartę.
        
        Args:
            suit (Suit): Kolor karty (kier, karo, trefl, pik)
            rank (Rank): Ranga karty (As, 2-10, Walet, Dama, Król)
            hidden (bool): Czy karta jest ukryta (domyślnie False)
        """
        self.suit = suit
        self.rank = rank
        self.hidden = hidden

    def is_rank_higher(self, other_card: 'Card') -> bool:
        """
        Sprawdza czy ranga tej karty jest wyższa od innej karty.
        
        Args:
            other_card (Card): Karta do porównania
            
        Returns:
            bool: True jeśli ranga tej karty jest wyższa
        """
        return self.rank.value > other_card.rank.value
    
    def is_same_suit(self, other_card: 'Card') -> bool:
        """
        Sprawdza czy ta karta ma ten sam kolor co inna karta.
        
        Args:
            other_card (Card): Karta do porównania
            
        Returns:
            bool: True jeśli karty mają ten sam kolor
        """
        return self.suit == other_card.suit
    
    def is_same_color(self, other_card: 'Card') -> bool:
        """
        Sprawdza czy ta karta ma ten sam kolor (czerwony/czarny) co inna karta.
        
        Args:
            other_card (Card): Karta do porównania
            
        Returns:
            bool: True jeśli karty mają ten sam kolor (czerwony/czarny)
        """
        return self.get_color() == other_card.get_color()
    
    def get_color(self):
        """
        Zwraca kolor karty (czerwony lub czarny).
        
        Returns:
            Color: RED dla kier i karo, BLACK dla trefl i pik
        """
        return Color.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Color.BLACK

    def __str__(self):
        """
        Zwraca tekstową reprezentację karty.
        
        Returns:
            str: Opis karty w formacie "Ranga of Kolor (KOLOR)" lub "??? of ????? (HIDDEN)"
        """
        if self.hidden:
            return "??? of ????? (HIDDEN)"
        return f"{self.rank.name} of {self.suit.name} ({self.get_color().name})"

    def clone(self) -> 'Card':
        """
        Tworzy kopię karty.
        
        Returns:
            Card: Nowa karta z takimi samymi właściwościami
        """
        return Card(self.suit, self.rank)
    
    def copy(self) -> 'Card':
        """
        Alias dla clone() - tworzy kopię karty.
        
        Returns:
            Card: Nowa karta z takimi samymi właściwościami
        """
        return self.clone()
    
def create_card(suit=None, rank=None, hidden=False) -> Card:
    """
    Tworzy nową kartę z opcjonalnymi parametrami.
    
    Jeśli kolor lub ranga nie są podane, zostaną wygenerowane losowo.
    
    Args:
        suit (Suit, optional): Kolor karty. Jeśli None, zostanie wylosowany
        rank (Rank, optional): Ranga karty. Jeśli None, zostanie wylosowana
        hidden (bool): Czy karta ma być ukryta (domyślnie False)
        
    Returns:
        Card: Nowa karta z podanymi lub wylosowanymi właściwościami
    """
    return Card(
        suit or get_random_suit(),
        rank or get_random_rank(),
        hidden=hidden
    )