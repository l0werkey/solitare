"""
Stan gry dla głównej rozgrywki pasjansa.
Obsługuje rysowanie planszy, nawigację kursorem i logikę transferu kart.
"""

from game_state import GameState
from ui.card_draw import draw_card, draw_card_top, draw_foundation_base
from core.card import create_card
import math
from time import time
import random
from core.transfer import TableauTransfer, StockTransfer, FoundationTransfer
import sys
from enum import Enum
from core.enums import Suit

BOARD_DETAILS = 50  # Liczba elementów dekoracyjnych na planszy

class CursorType(Enum):
    """
    Enum definiujący typy kursorów na planszy gry.
    """
    TABLEAU = 0      # Kursor w obszarze tableau (głównej planszy)
    STOCK = 1        # Kursor w obszarze talii kart
    FOUNDATION = 2   # Kursor w obszarze fundamentów

    @classmethod
    def get_type(cls, name: str):
        """
        Zwraca typ kursora na podstawie nazwy.
        
        Args:
            name (str): Nazwa typu kursora
            
        Returns:
            CursorType lub None: Typ kursora lub None jeśli nie znaleziono
        """
        return getattr(cls, name.upper(), None)

    @classmethod
    def is_valid(cls, value):
        """
        Sprawdza czy wartość jest prawidłowym typem kursora.
        
        Args:
            value: Wartość do sprawdzenia
            
        Returns:
            bool: True jeśli wartość jest prawidłowa
        """
        return value in cls.__members__.values()

class PlayState(GameState):
    """
    Główny stan gry obsługujący rozgrywkę pasjansa.
    
    Zarządza wyświetlaniem planszy, nawigacją kursorem,
    obsługą wejścia użytkownika i transferami kart.
    """
    
    def __init__(self, id: str, difficulty=None):
        """
        Inicjalizuje nowy stan rozgrywki.
        
        Args:
            id (str): Identyfikator stanu
        """
        super().__init__(id)
        self.seed = hash(time()) % (10**8)  # Ziarno dla generowania dekoracji
        self.cursor = (0, 0)                # Pozycja kursora (x, y)
        self.cursor_type = CursorType.TABLEAU  # Aktualny typ kursora
        self.frame = 0                      # Licznik klatek dla animacji
        self.transfer_a = None              # Pierwszy transfer (źródło)
        self.transfer_b = None              # Drugi transfer (cel)
        self.blink = False                  # Flaga migania

        self.global_timer = 0               # Globalny timer

        self.transfer_a_origin = (0, 0)     # Pozycja początkowa transferu

        self.toasts = []

        self.dif = difficulty


    def init(self):
        self.get_owner().reset_game(difficulty=self.dif)

        
    def get_focused_card(self):
        """
        Zwraca kartę aktualnie wskazywaną przez kursor.
        
        Returns:
            Card lub None: Aktualnie fokusowana karta lub None
        """
        game = self.get_owner().get_game()
        cursor = self.get_real_cursor()
        pile = game.tableau.piles[cursor[0]]
        if pile is None:
            return None
        card = pile.as_list()[cursor[1]]

        return card

    def get_real_cursor(self):
        """
        Zwraca rzeczywistą pozycję kursora z uwzględnieniem granic planszy.
        
        Koryguje pozycję kursora aby mieściła się w granicach planszy
        i pomija ukryte karty.
        
        Returns:
            tuple: Skorygowana pozycja kursora (x, y)
        """
        game = self.get_owner().get_game()
        new_x = self.cursor[0]
        new_y = self.cursor[1]
        if new_x < 0:
            new_x = 0
        if new_x >= len(game.tableau.piles):
            new_x = len(game.tableau.piles) - 1
        if new_y < 0:
            new_y = 0
            
        # Sprawdź długość stosu tylko jeśli stos nie jest None
        if new_x < len(game.tableau.piles) and game.tableau.piles[new_x] is not None:
            if new_y >= len(game.tableau.piles[new_x].as_list()):
                new_y = len(game.tableau.piles[new_x].as_list()) - 1
        else:
            # Dla pustych stosów ustaw y na 0
            new_y = 0
            
        if new_x >= 0 and new_x < len(game.tableau.piles):
            pile = game.tableau.piles[new_x]
            if pile is not None:
                cards = pile.as_list()
                for i, card in enumerate(cards):
                    if i < new_y:
                        continue
                    if card.hidden:
                        new_y += 1
                    else:
                        break
        return (new_x, new_y)

    
    def draw(self, term, screen):
        """
        Rysuje kompletną planszę gry na ekranie.
        
        Rysuje tło, dekoracje, wszystkie elementy gry (stock, fundamenty, tableau)
        i aktualizuje liczniki animacji.
        
        Args:
            term: Instancja terminala do formatowania
            screen: Bufor ekranu do rysowania
        """
        screen.bg(term.on_darkgreen + " " + term.normal)

        for i in range(BOARD_DETAILS):
            random.seed(self.seed + i)
            max_w = term.width
            max_h = term.height

            x = random.randint(0, max_w - 1)
            y = random.randint(0, max_h - 1)

            screen.set_char(x, y, term.on_darkgreen + term.green + "~" + term.normal)

        self.blink = self.frame % 30 < 10

        self.draw_stock(term, screen)
        self.draw_foundations(term, screen)
        self.draw_tableau(term, screen, x_off=14)

        if self.transfer_a is not None and self.cursor_type == CursorType.FOUNDATION and self.global_timer % 20 < 10:
            x_a, y_a = self.transfer_a_origin
            x_b, y_b = (screen.width-12, self.cursor[1]*7+4)
            screen.line(x_b, y_b, x_a, y_a, term.on_yellow + term.white + " " + term.normal)

        for i, toast in enumerate(self.toasts):
            screen.insert_line(0, screen.height - 1 - i, toast, prefix=term.on_black + term.white, suffix=term.normal)

        if self.global_timer % 20 == 0:
            if len(self.toasts) > 0:
                self.toasts.pop(0)

        self.global_timer += 1

        


    def draw_stock(self, term, screen):
        """
        Rysuje obszar talii kart (stock) po lewej stronie ekranu.
        
        Args:
            term: Instancja terminala do formatowania
            screen: Bufor ekranu do rysowania
        """

        screen.rect(0, 0, 13, screen.height, term.on_black + " " + term.normal)

        game = self.get_owner().get_game()

        dummy_card = create_card()
        dummy_card.hidden = True

        for y in range(2):
            draw_card(term, screen, dummy_card, x=1, y=1-y, invert=(self.cursor[1]==0 and self.blink and self.cursor_type == CursorType.STOCK))

        cards = game.stock.get_waste(game.difficulty)
        for y, card in enumerate(cards):
            if y == len(cards) - 1:
                draw_card(term, screen, card, x=1, y=9+y, invert=(self.cursor[1]==1 and self.blink and self.cursor_type == CursorType.STOCK))
            else:
                draw_card_top(term, screen, card, x=1, y=9+y)
                
    def draw_foundations(self, term, screen):
        """
        Rysuje obszar fundamentów po prawej stronie ekranu.
        
        Args:
            term: Instancja terminala do formatowania
            screen: Bufor ekranu do rysowania
        """

        screen.rect(screen.width-13, 0, 13, screen.height, term.on_black + " " + term.normal)

        game = self.get_owner().get_game()

        for y, suit in enumerate(Suit):
            should_blink = self.blink and self.cursor_type == CursorType.FOUNDATION and self.cursor[1] == y
            draw_foundation_base(term, screen, suit, x=screen.width-12, y=y*7, invert=should_blink)

        for x, foundation in enumerate(game.foundations.get_all()):
            if foundation is None:
                continue

            cards = foundation.as_list()
            if len(cards) == 0:
                continue

            card = cards[-1]
            should_blink = self.blink and self.get_focused_card() == card and self.cursor_type == CursorType.FOUNDATION

            if len(cards) == 1:
                draw_card(term, screen, card, x=screen.width-12, y=x*7, invert=should_blink)
            else:
                draw_card_top(term, screen, card, x=screen.width-12, y=x*7, invert=should_blink) 

    def draw_tableau(self, term, screen, x_off=0):
        """
        Rysuje główną planszę gry (tableau) w środkowej części ekranu.
        
        Args:
            term: Instancja terminala do formatowania
            screen: Bufor ekranu do rysowania
            x_off (int): Przesunięcie w poziomie
        """

        for x, pile in enumerate(self.get_owner().get_game().tableau.piles):
            if pile is None:
                continue

            cards = pile.as_list()

            for y, card in enumerate(cards):
                should_blink = self.blink and self.get_focused_card() == card and self.cursor_type == CursorType.TABLEAU

                if len(cards) == y + 1:
                    draw_card(term, screen, card, x=x*12+x_off, y=y+1, invert=should_blink)
                else:
                    draw_card_top(term, screen, card, x=x*12+x_off, y=y+1, invert=should_blink)
                
                if self.get_focused_card() == card and self.transfer_a is not None and self.global_timer % 20 < 10 and self.cursor_type == CursorType.TABLEAU:
                    screen.line(self.transfer_a_origin[0], self.transfer_a_origin[1], x*12+x_off+5, y+4, term.on_yellow + term.white + " " + term.normal)
        
        for x, pile in enumerate(self.get_owner().get_game().tableau.piles):
            if pile is None:
                continue

            cards = pile.as_list()
            for y, card in enumerate(cards):
                if self.get_focused_card() == card and self.transfer_a is not None and self.global_timer % 20 < 10 and self.cursor_type == CursorType.TABLEAU:
                    screen.line(self.transfer_a_origin[0], self.transfer_a_origin[1], x*12+x_off+5, y+4, term.on_yellow + term.white + " " + term.normal)
        
        focused_card = self.get_focused_card()
        if focused_card and not focused_card.hidden and self.frame > 50 and self.cursor_type == CursorType.TABLEAU:
            x, y = self.get_real_cursor()
            screen.insert_line(x*12+3+x_off, y+8, str(focused_card), prefix=term.on_black + term.white, suffix=term.normal)

        self.frame += 1

    def clamp_cursor(self):
        """
        Ogranicza pozycję kursora do prawidłowych wartości.
        
        Aktualizuje pozycję kursora używając get_real_cursor()
        aby zapewnić że kursor znajduje się w prawidłowych granicach.
        """
        self.cursor = self.get_real_cursor()
        
    def handle_cursor_for_foundation(self, input):
        """
        Obsługuje ruch kursora w obszarze fundamentów.
        
        Args:
            input: Wciśnięty klawisz od użytkownika
        """
        if input.name == 'KEY_LEFT':
            self.cursor_type = CursorType.TABLEAU
            self.cursor = (6, 0)
            while self.get_owner().get_game().tableau.piles[self.cursor[0]] is None and self.cursor[0] > 0:
                self.cursor = (self.cursor[0] - 1, self.cursor[1])
            self.frame = 0
            self.clamp_cursor()
        elif input.name == 'KEY_DOWN':
            if self.cursor[1] < 3:
                self.cursor = (self.cursor[0], self.cursor[1] + 1)
            else:
                self.cursor = (self.cursor[0], 0)
            self.frame = 0
        elif input.name == 'KEY_UP':
            if self.cursor[1] > 0:
                self.cursor = (self.cursor[0], self.cursor[1] - 1)
            else:
                self.cursor = (self.cursor[0], len(Suit) - 1)
            self.frame = 0

        if input.name == 'KEY_ENTER':
            if self.transfer_a is None:
                self.transfer_a = FoundationTransfer(
                    foundations=self.get_owner().get_game().foundations,
                    target_index=self.cursor[1],
                    difficulty=self.get_owner().get_game().difficulty
                )
                x, y = self.get_real_cursor()
                self.transfer_a_origin = (x * 12 + 14 + 5, y + 4)
            elif self.transfer_b is None:
                self.transfer_b = FoundationTransfer(
                    foundations=self.get_owner().get_game().foundations,
                    target_index=self.cursor[1],
                    difficulty=self.get_owner().get_game().difficulty
                )

                game = self.get_owner().get_game()
                success = game.transfer(self.transfer_a, self.transfer_b)
                self.transfer_a = None
                self.transfer_b = None
                if not success:
                    self.toasts.append("Invalid move. Try again.")
                else:
                    # If the transfer was successful, reset cursor to tableau
                    self.cursor_type = CursorType.TABLEAU
                    self.cursor = (0, 0)
                    self.frame = 0
                    self.clamp_cursor()

    def handle_cursor_for_tableau(self, input):
        """
        Obsługuje ruch kursora w obszarze tableau (głównej planszy).
        
        Umożliwia nawigację między stosami kart, wybór kart do przeniesienia
        i wykonywanie transferów między stosami.
        
        Args:
            input: Wciśnięty klawisz od użytkownika
        """
        if input.name == 'KEY_RIGHT':
            # Check if we're at the rightmost pile and should go to foundation
            game = self.get_owner().get_game()
            if self.cursor[0] >= len(game.tableau.piles) - 1:
                # We're at or beyond the last pile, check if we can find a non-empty pile to the right
                found_pile = False
                for i in range(self.cursor[0] + 1, len(game.tableau.piles)):
                    if game.tableau.piles[i] is not None:
                        self.cursor = (i, self.cursor[1])
                        self.frame = 0
                        self.clamp_cursor()
                        found_pile = True
                        break
                
                if not found_pile:
                    # No more non-empty piles to the right, go to foundation
                    self.cursor_type = CursorType.FOUNDATION
                    self.cursor = (0, 0)
                    self.frame = 0
            else:
                # Normal right movement
                self.cursor = (self.cursor[0] + 1, self.cursor[1])
                self.frame = 0
                self.clamp_cursor()
                # Skip over empty piles when moving right
                while (self.cursor[0] < len(game.tableau.piles) - 1 and 
                       game.tableau.piles[self.cursor[0]] is None):
                    self.cursor = (self.cursor[0] + 1, self.cursor[1])
                    self.clamp_cursor()
                
                # If we ended up at the last pile and it's empty, or beyond bounds, go to foundation
                if (self.cursor[0] >= len(game.tableau.piles) - 1 and
                    (self.cursor[0] >= len(game.tableau.piles) or 
                     game.tableau.piles[self.cursor[0]] is None)):
                    self.cursor_type = CursorType.FOUNDATION
                    self.cursor = (0, 0)
                    self.frame = 0
        elif input.name == 'KEY_LEFT':
            if self.cursor[0] == 0:
                self.cursor_type = CursorType.STOCK
                self.cursor = (0, 0)
                self.frame = 0
                self.transfer_a = None
                self.transfer_b = None
                return
            self.cursor = (self.cursor[0] - 1, self.cursor[1])
            self.frame = 0
            self.clamp_cursor()
            game = self.get_owner().get_game()
            while (self.cursor[0] > 0 and 
                   game.tableau.piles[self.cursor[0]] is None):
                self.cursor = (self.cursor[0] - 1, self.cursor[1])
                self.clamp_cursor()
            if self.cursor[0] == 0 and game.tableau.piles[self.cursor[0]] is None:
                self.cursor_type = CursorType.STOCK
                self.cursor = (0, 0)
                self.frame = 0
                self.transfer_a = None
                self.transfer_b = None
        elif input.name == 'KEY_DOWN':
            self.cursor = (self.cursor[0], self.cursor[1] + 1) 
            self.frame = 0
            self.clamp_cursor()
        elif input.name == 'KEY_UP':
            self.cursor = (self.cursor[0], self.cursor[1] - 1)
            self.frame = 0
            self.clamp_cursor()

        if input.name == 'KEY_ENTER':
            game = self.get_owner().get_game()
            cursor_pos = self.get_real_cursor()

            if self.transfer_a is None:
                self.transfer_a = TableauTransfer(
                    tableau=game.tableau,
                    source_index=cursor_pos[0],
                    depth=cursor_pos[1],
                    difficulty=game.difficulty
                )

                x, y = self.get_real_cursor()
                self.transfer_a_origin = (x * 12 + 14 + 5, y + 4)

            elif self.transfer_b is None:
                self.transfer_b = TableauTransfer(
                    tableau=game.tableau,
                    source_index=cursor_pos[0],
                    depth=cursor_pos[1],
                    difficulty=game.difficulty
                )

                success = game.transfer(self.transfer_a, self.transfer_b)
                self.transfer_a = None
                self.transfer_b = None
                if not success:
                    self.toasts.append("Invalid move. Try again.")

    def handle_cursor_for_stock(self, input):
        """
        Obsługuje ruch kursora w obszarze talii kart (stock).
        
        Umożliwia przełączanie między talią a stosem odrzutowym,
        oraz dobieranie nowych kart.
        
        Args:
            input: Wciśnięty klawisz od użytkownika
        """
        if input.name == 'KEY_RIGHT':
            self.cursor_type = CursorType.TABLEAU
            self.cursor = (0, 0)
            while self.get_owner().get_game().tableau.piles[self.cursor[0]] is None and self.cursor[0] < len(self.get_owner().get_game().tableau.piles) - 1:
                self.cursor = (self.cursor[0] + 1, self.cursor[1])
            self.frame = 0
            self.clamp_cursor()
        elif input.name == 'KEY_DOWN' or input.name == 'KEY_UP':
            if self.cursor[1] == 0:
                self.cursor = (0, 1)
            else:
                self.cursor = (0, 0)
            self.frame = 0

        if input.name == 'KEY_ENTER':
            if self.cursor[1] == 0:
                game = self.get_owner().get_game()
                game.stock.draw_cards(game.difficulty)
                self.frame = 0
            elif self.cursor[1] == 1:
                game = self.get_owner().get_game()
                placed = False
                for x in range(3):
                    placed = game.transfer(StockTransfer(game.stock, game.difficulty), FoundationTransfer(
                        foundations=game.foundations,
                        target_index=x,
                        difficulty=game.difficulty
                    ))
                    if placed:
                        self.cursor_type = CursorType.TABLEAU
                        self.cursor = (x, 0)
                        self.frame = 0
                        self.clamp_cursor()
                        placed = True
                        break
                if not placed:
                    for x in range(len(game.tableau.piles)):
                        placed = game.transfer(StockTransfer(game.stock, game.difficulty), TableauTransfer(
                            tableau=game.tableau,
                            source_index=x,
                            depth=0,
                            difficulty=game.difficulty
                        ))
                        if placed:
                            self.cursor_type = CursorType.TABLEAU
                            self.cursor = (x, 0)
                            self.frame = 0
                            self.clamp_cursor()
                            break
                        else:
                            self.toasts.append("No valid moves available.")
            

    def on_input(self, term, input):
        """
        Główna metoda obsługująca wejście użytkownika.
        
        Deleguje obsługę klawiszy do odpowiednich metod w zależności
        od aktualnego typu kursora i obsługuje globalne skróty klawiszowe.
        
        Args:
            term: Instancja terminala
            input: Wciśnięty klawisz od użytkownika
        """
        if input == 'q':
            self.get_owner().running = False

        if input == 'z':
            try:
                self.get_owner().undo()
            except ValueError as e:
                self.toasts.append(str(e))

        if self.cursor_type == CursorType.TABLEAU:
            self.handle_cursor_for_tableau(input)

        elif self.cursor_type == CursorType.STOCK:
            self.handle_cursor_for_stock(input)

        elif self.cursor_type == CursorType.FOUNDATION:
            self.handle_cursor_for_foundation(input)

        if self.get_owner().get_game().has_won():
            sys.exit(0)
            print("You won!")

