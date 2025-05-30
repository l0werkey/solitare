"""
Główna klasa zarządzająca grą i stanami.
Odpowiada za zarządzanie stanem gry, renderowanie, obsługę wejścia i historię ruchów.
"""

from core.game import SolitareGame
from blessed import Terminal
from ui.screen import Screen
from core.enums import Difficulty, Time
import dill
import os
from transition_manager import TransitionManager
import sys
import random
import time
from menu_state import MenuState

class GameWrapper:
    """
    Główny wrapper gry odpowiedzialny za zarządzanie stanami i główną pętlą gry.
    
    Klasa zarządza przełączaniem między stanami gry, obsługuje terminal,
    ekran oraz funkcjonalność cofania ruchów.
    """
    
    def __init__(self):
        """
        Inicjalizuje nową instancję GameWrapper.
        
        Tworzy nową grę pasjansa, inicjalizuje terminal i ekran,
        oraz przygotowuje listę na historię stanów gry.
        """
        self._current_state = None
        self._game = SolitareGame(difficulty=Difficulty.HARD, transfer_listener=self.create_on_transfer())
        self.last_game_states = []
        self._term = Terminal()
        self._screen = Screen(self._term.width, self._term.height)
        self.running = True
        self.transition_manager = TransitionManager(self)

    def set_state(self, state, force=False) -> None:
        """
        Ustawia nowy stan gry.
        
        Jeśli już istnieje aktywny stan, zostaje on zastąpiony nowym.
        Nowy stan otrzymuje referencję do tego GameWrapper i aktualnej gry.
        
        Args:
            state: Nowy stan gry do ustawienia
        """
        if self._current_state is state:
            return
            
        if not force:
            self.transition_manager.begin(self._screen, state)
        else:
            if self._current_state is not None:
                self._current_state.set_as_owner(None)
            self._current_state = state
            self._current_state.set_as_owner(self)

            self._current_state.set_game(self._game)

            self._current_state.init()

            self._screen.clear()
            self._current_state.draw(self._term, self._screen)

    def menu(self):
        """
        Ustawia stan menu gry.
        
        Tworzy nową instancję MenuState i ustawia ją jako aktualny stan gry.
        """
        menu_state = MenuState("menu_state")
        self.set_state(menu_state)


    def get_game(self) -> SolitareGame:
        """
        Zwraca aktualną instancję gry.
        
        Returns:
            SolitareGame: Aktualna gra pasjansa
        """
        return self._game
    
    def get_current_state(self):
        """
        Zwraca aktualny stan gry.
        
        Returns:
            Aktualny stan gry
            
        Raises:
            ValueError: Jeśli stan nie został ustawiony
        """
        if self._current_state is None:
            raise ValueError("Current state is not set.")
        return self._current_state
    
    def reset_game(self, difficulty=Difficulty.EASY) -> None:
        """
        Resetuje grę do stanu początkowego.
        
        Tworzy nową instancję gry z podanym poziomem trudności
        i odświeża wyświetlanie.
        
        Args:
            difficulty: Poziom trudności nowej gry (domyślnie EASY)
        """
        self._game = SolitareGame(difficulty=difficulty, transfer_listener=self.create_on_transfer())
        if self._current_state is not None:
            self._current_state.draw(self._term, self._screen)

    def save_state(self) -> None:
        """
        Zapisuje aktualny stan gry do historii.
        
        Zachowuje maksymalnie 3 ostatnie stany gry dla funkcji cofania.
        Starsze stany są automatycznie usuwane.
        """
        self.last_game_states.append(self._game.copy())
        if len(self.last_game_states) > 3:
            self.last_game_states.pop(0)

    def create_on_transfer(self):
        """
        Tworzy funkcję callback dla transferów w grze.
        
        Returns:
            function: Funkcja obsługująca zdarzenia transferu kart
        """
        wrapper = self
        def on_transfer(time: Time):
            """
            Obsługuje zdarzenia transferu kart.
            
            Args:
                time (Time): Moment transferu (PRE_MOVE lub POST_MOVE)
            """
            if time == Time.PRE_MOVE:
                wrapper.save_state()
            elif time == Time.POST_MOVE:
                self.save_game()

        return on_transfer
    
    def undo(self) -> None:
        """
        Cofa ostatni ruch w grze.
        
        Przywraca poprzedni stan gry z historii i odświeża wyświetlanie.
        
        Raises:
            ValueError: Jeśli nie ma ruchów do cofnięcia
        """
        if self.last_game_states:
            self._game = self.last_game_states.pop()
            if self._current_state is not None:
                self._current_state.draw(self._term, self._screen)
        else:
            raise ValueError("Nothing to undo...")

    def run(self):
        """
        Uruchamia główną pętlę gry.
        
        Inicjalizuje tryb pełnoekranowy terminala, ukrywa kursor
        i rozpoczyna główną pętlę obsługującą wejście i renderowanie.
        Pętla działa dopóki self.running jest True.
        """
        print(self._term.clear)
        with self._term.cbreak(), self._term.hidden_cursor(), self._term.fullscreen():
            while self.running:
                if self._current_state is not None:
                    input = self._term.inkey(timeout=0.02)
                    if input and not self.transition_manager.began():
                        self._current_state.on_input(self._term, input)

                    random.seed(time.time())
                    for x in range(16):
                        if self.transition_manager.began():
                            if self.transition_manager.complete:
                                self.transition_manager.reduct()
                            else:
                                self.transition_manager.expand()


                    self._screen.clear()
                    self._current_state.draw(self._term, self._screen)
                    self.transition_manager.render(self._screen, self._term)
                    self._screen.render(self._term, 0, 0)

        print(self._term.clear)
        print("Thanks for playing!")

    def was_game_saved(self) -> bool:
        """
        Sprawdza, czy gra została zapisana.
        Returns:
            bool: True jeśli gra została zapisana, False w przeciwnym razie
        """
        return os.path.exists("save.bin")
    
    def save_game(self) -> None:
        """
        Zapisuje aktualny stan gry do pliku.
        
        Serializuje obiekt gry i zapisuje go do pliku 'save.bin'.
        """
        self._game.transfer_listener = None
        with open("save.bin", "wb") as f:
            dill.dump(self._game, f)
        self._game.transfer_listener = self.create_on_transfer()

    def load_game(self) -> None:
        """
        Ładuje stan gry z pliku.
        
        Deserializuje obiekt gry z pliku 'save.bin' i ustawia go jako aktualny stan gry.
        
        Raises:
            FileNotFoundError: Jeśli plik 'save.bin' nie istnieje
        """

        if not os.path.exists("save.bin"):
            raise FileNotFoundError("Save file not found.")
        with open("save.bin", "rb") as f:
            self._game = dill.load(f)
            print(dill.load(f))
        self._game.transfer_listener = self.create_on_transfer()

