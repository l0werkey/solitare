"""
Bazowa klasa stanu gry.
Definiuje interfejs dla różnych stanów gry i zarządza powiązaniami z GameWrapper.
"""

from blessed.keyboard import Keystroke
from blessed import Terminal
from game_wrapper import GameWrapper
from ui.screen import Screen

class GameState:
    """
    Abstrakcyjna klasa bazowa reprezentująca stan gry.
    
    Każdy konkretny stan gry (np. menu, rozgrywka) powinien dziedziczyć po tej klasie
    i implementować metody on_input() oraz draw().
    """
    
    def __init__(self, id: str):
        """
        Inicjalizuje nowy stan gry.
        
        Args:
            id (str): Unikalny identyfikator stanu gry
        """
        self.id = id
        self._state_manager = None
        self._game = None

    def set_game(self, game) -> None:
        """
        Ustawia instancję gry dla tego stanu.
        
        Args:
            game: Instancja gry do przypisania
        """
        self._game = game

    def init(self):
        pass

    def get_game(self):
        """
        Zwraca przypisaną instancję gry.
        
        Returns:
            Instancja gry
            
        Raises:
            ValueError: Jeśli gra nie została ustawiona
        """
        if self._game is None:
            raise ValueError("Game is not set.")
        return self._game

    def get_owner(self) -> GameWrapper:
        """
        Zwraca właściciela tego stanu (GameWrapper).
        
        Returns:
            GameWrapper: Instancja zarządzająca stanem
            
        Raises:
            ValueError: Jeśli właściciel nie został zainicjalizowany
        """
        if self._state_manager is None:
            raise ValueError("State manager is not initialized.")
        return self._state_manager

    def set_as_owner(self, state_manager: GameWrapper) -> None:
        """
        Ustawia właściciela tego stanu.
        
        Args:
            state_manager (GameWrapper): Nowy właściciel stanu
            
        Raises:
            ValueError: Jeśli stan już ma właściciela
        """
        if self._state_manager is not None:
            raise ValueError("This state already has an owner.")
        self._state_manager = state_manager

    def on_input(self, term: Terminal, input: Keystroke) -> None:
        """
        Obsługuje wejście użytkownika.
        
        Metoda abstrakcyjna - musi być zaimplementowana przez klasy dziedziczące.
        
        Args:
            term (Terminal): Instancja terminala
            input (Keystroke): Wciśnięty klawisz
            
        Raises:
            NotImplementedError: Jeśli nie została zaimplementowana
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def draw(self, term: Terminal, screen: Screen) -> None:
        """
        Rysuje stan gry na ekranie.
        
        Metoda abstrakcyjna - musi być zaimplementowana przez klasy dziedziczące.
        
        Args:
            term (Terminal): Instancja terminala
            screen (Screen): Bufor ekranu do rysowania
            
        Raises:
            NotImplementedError: Jeśli nie została zaimplementowana
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_id(self) -> str:
        """
        Zwraca identyfikator stanu.
        
        Returns:
            str: Identyfikator stanu
        """
        return self.id