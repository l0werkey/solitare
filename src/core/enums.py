"""
Definicje enumeracji używanych w grze pasjans.
Zawiera kolory kart, rangi, trudności gry i typy transferów.
"""

from enum import Enum, auto

class Suit(Enum):
    """
    Enum reprezentujący kolory kart.
    """
    HEARTS = auto()    # Kiery
    DIAMONDS = auto()  # Karo
    CLUBS = auto()     # Trefl
    SPADES = auto()    # Piki

    def __str__(self):
        """
        Zwraca symbol Unicode dla koloru karty.
        
        Returns:
            str: Symbol koloru (♥, ♦, ♣, ♠)
        """
        return {
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣",
            Suit.SPADES: "♠"
        }[self]

class Rank(Enum):
    """
    Enum reprezentujący rangi kart od Asa do Króla.
    """
    ACE = 0      # As
    TWO = 1      # Dwójka
    THREE = 2    # Trójka
    FOUR = 3     # Czwórka
    FIVE = 4     # Piątka
    SIX = 5      # Szóstka
    SEVEN = 6    # Siódemka
    EIGHT = 7    # Ósemka
    NINE = 8     # Dziewiątka
    TEN = 9      # Dziesiątka
    JACK = 10    # Walet
    QUEEN = 11   # Dama
    KING = 12    # Król

    def __str__(self):
        """
        Zwraca polską nazwę rangi karty.
        
        Returns:
            str: Polska nazwa rangi
        """
        return {
            Rank.ACE: "As",
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "Walet",
            Rank.QUEEN: "Dama",
            Rank.KING: "Król"
        }[self]
    
    def short_name(self):
        """
        Zwraca skróconą nazwę rangi karty.
        
        Returns:
            str: Skrócona nazwa rangi (A, 2-10, J, Q, K)
        """
        return {
            Rank.ACE: "A",
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K"
        }[self]

class Color(Enum):
    """
    Enum reprezentujący kolory kart (czerwony/czarny).
    """
    RED = auto()    # Czerwony (kiery, karo)
    BLACK = auto()  # Czarny (trefl, piki)

class Difficulty(Enum):
    """
    Enum reprezentujący poziomy trudności gry.
    """
    EASY = auto()  # Łatwy (dobieranie po 1 karcie)
    HARD = auto()  # Trudny (dobieranie po 3 karty)

    def __str__(self):
        """
        Zwraca polską nazwę poziomu trudności.
        
        Returns:
            str: "Łatwy" lub "Trudny"
        """
        return "Łatwy" if self == Difficulty.EASY else "Trudny"
    
class TransferContext(Enum):
    """
    Enum określający kontekst transferu (źródło lub cel).
    """
    FROM = "from"  # Źródło transferu
    TO = "to"      # Cel transferu

class TransferType(Enum):
    """
    Enum reprezentujący typy transferów między obszarami gry.
    """
    TABLEAU = "tableau"      # Transfer w obrębie tableau
    STOCK = "stock"          # Transfer z/do talii
    FOUNDATION = "foundation" # Transfer z/do fundamentów

    def __str__(self):
        """
        Zwraca sformatowaną nazwę typu transferu.
        
        Returns:
            str: Nazwa typu z pierwszą wielką literą
        """
        return self.value.capitalize()
    
    @property
    def is_tableau(self) -> bool:
        """
        Sprawdza czy transfer dotyczy tableau.
        
        Returns:
            bool: True jeśli typ to TABLEAU
        """
        return self == TransferType.TABLEAU
    
    @property
    def is_stock(self) -> bool:
        """
        Sprawdza czy transfer dotyczy talii.
        
        Returns:
            bool: True jeśli typ to STOCK
        """
        return self == TransferType.STOCK
    
    @property
    def is_foundation(self) -> bool:
        """
        Sprawdza czy transfer dotyczy fundamentów.
        
        Returns:
            bool: True jeśli typ to FOUNDATION
        """
        return self == TransferType.FOUNDATION
    
class Time(Enum):
    """
    Enum reprezentujący momenty w czasie transferu.
    """
    POST_MOVE = "post_move"  # Po wykonaniu ruchu
    PRE_MOVE = "pre_move"    # Przed wykonaniem ruchu
    