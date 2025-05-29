"""
Moduł zawierający główną klasę gry Pasjans (Solitaire).

Ten moduł implementuje główną logikę gry pasjans, łącząc wszystkie elementy
gry takie jak tableau, stock, fundamenty i system transferu kart.
"""

from core.tableau import Tableau
from core.card import Card, create_card
from core.difficulty import Difficulty
from core.stock import Stock
from core.foundations import Foundations
from core.enums import Suit, Rank, Color, TransferContext, Time
from core.transfer import Transfer, TableauTransfer, StockTransfer, FoundationTransfer
from core.pile_part import create_pile
from time import time
import random 
from typing import Callable, Optional, Union

class SolitareGame:
    """
    Główna klasa gry Pasjans (Solitaire).
    
    Zarządza wszystkimi elementami gry: tableau (główne stosy kart), 
    stock (talia do ciągnięcia), fundamenty (stosy finałowe) oraz 
    system transferu kart między różnymi stosami.
    
    Attributes:
        tableau (Tableau): Główne stosy kart na planszy
        stock (Stock): Talia kart do ciągnięcia
        foundations (Foundations): Stosy finałowe podzielone według kolorów
        difficulty (Difficulty): Poziom trudności gry
        transfer_listener (Callable): Funkcja nasłuchująca transferów kart
    """
    
    def __init__(self, difficulty: Difficulty, transfer_listener: Callable[[Time], None]):
        """
        Inicjalizuje nową grę pasjans.
        
        Args:
            difficulty (Difficulty): Poziom trudności gry
            transfer_listener (Callable[[Time], None]): Funkcja wywoływana 
                przed i po każdym ruchu kart
        """
        self.tableau = Tableau()
        self.stock = Stock()
        self.foundations = Foundations()
        self.difficulty = difficulty
        self.transfer_listener = transfer_listener

        random.seed(time())

        self._setup_game()

    def _assemble_tableau(self):
        """
        Układa karty na tableau zgodnie z regułami pasjansa.
        
        Rozdaje karty z stock do stosów tableau - pierwszy stos otrzymuje 1 kartę,
        drugi 2 karty, trzeci 3 karty itd. Wszystkie karty oprócz ostatniej
        w każdym stosie są ukryte.
        """
        for i in range(Tableau.PILE_COUNT):
            for j in range(i + 1):
                card = self.stock.remove_random_card()
                if card:
                    card.hidden = (j != i)
                    if self.tableau.piles[i] is None:

                        self.tableau.piles[i] = create_pile(card)
                    else:
                        self.tableau.piles[i].add_card(card)

    def _setup_game(self):
        """
        Konfiguruje początkowy stan gry.
        
        Układa karty na tableau i przygotowuje stock do gry.
        """
        self._assemble_tableau()
        self.stock.draw_cards()    
        
    def _patch_difficulty(self, source: Transfer, target: Transfer):
        """
        Aplikuje poziom trudności do obiektów transferu.
        
        Args:
            source (Transfer): Źródłowy obiekt transferu
            target (Transfer): Docelowy obiekt transferu
        """
        source.difficulty = self.difficulty
        target.difficulty = self.difficulty    
    
    def transfer(self, source: Transfer, target: Transfer) -> bool:
        """
        Wykonuje transfer kart między stosami.
        
        Sprawdza czy transfer jest możliwy, wykonuje go jeśli tak,
        i powiadamia nasłuchiwacza o ruchu.
        
        Args:
            source (Transfer): Źródłowy obiekt transferu
            target (Transfer): Docelowy obiekt transferu
            
        Returns:
            bool: True jeśli transfer został wykonany pomyślnie, False w przeciwnym razie
        """
        self._patch_difficulty(source, target)

        if isinstance(source, TableauTransfer) and source.source_index >= 0:
            if source.tableau.piles[source.source_index] is None:
                return False

        offer = source.create_offer(target.get_type())
        if offer is None:
            return False
        if not target.verify_offer(offer):
            return False
        self.transfer_listener(Time.PRE_MOVE)
        offer.complete()
        self.transfer_listener(Time.POST_MOVE)
        return True
    
    def can_transfer(self, source: Transfer, target: Transfer) -> bool:
        """
        Sprawdza czy transfer między stosami jest możliwy bez jego wykonywania.
        
        Args:
            source (Transfer): Źródłowy obiekt transferu
            target (Transfer): Docelowy obiekt transferu
            
        Returns:
            bool: True jeśli transfer jest możliwy, False w przeciwnym razie
        """
        self._patch_difficulty(source, target)
        offer = source.create_offer(target.get_type())
        if offer is None:
            return False
        return target.verify_offer(offer)

    def get_difficulty(self) -> Difficulty:
        """
        Zwraca aktualny poziom trudności gry.
        
        Returns:
            Difficulty: Poziom trudności gry        """
        return self.difficulty
    
    def copy(self) -> 'SolitareGame':
        """
        Tworzy głęboką kopię gry.
        
        Returns:
            SolitareGame: Nowa instancja gry będąca kopią aktualnej
        """
        new_game = SolitareGame(self.difficulty, self.transfer_listener)
        new_game.tableau = self.tableau.copy()
        new_game.stock = self.stock.copy()
        new_game.foundations = self.foundations.copy()
        return new_game
    
    def has_won(self) -> bool:
        """
        Sprawdza czy gracz wygrał grę.
        
        Gra jest wygrana gdy wszystkie stosy są poprawnie ułożone:
        - Tableau: wszystkie stosy są puste lub posortowane
        - Fundamenty: wszystkie stosy są kompletne i posortowane
        - Stock: jest pusty
        
        Returns:
            bool: True jeśli gra została wygrana, False w przeciwnym razie
        """
        tableau_complete = all(pile is None or pile.is_sorted() for pile in self.tableau.piles)
        foundations_complete = all(foundation.is_sorted() for foundation in self.foundations.get_all())
        stock_complete = self.stock.is_empty()

        return tableau_complete and foundations_complete and stock_complete