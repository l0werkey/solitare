from ui.screen import Screen
import random
from blessed import Terminal
from core.card import create_card
from ui.card_draw import draw_card
import sys
import time

class TransitionManager:
    def __init__(self, wrapper=None):
        self.possible_posses = []
        self.cards = []
        self.target = None
        self.complete = True
        self.wrapper = wrapper

    def reduct(self):
        """
        Reduces the number of cards in the transition.
        """
        if self.cards:
            self.cards.pop()

    def begin(self, screen: Screen, state):
        """
        Begins a new transition by clearing the current cards.
        """
        self.cards.clear()
        self.complete = False
        for x in range(-20, screen.width+20, 9):
            for y in range(-8, screen.height+8, 5):
                self.possible_posses.append((x, y))
        random.seed(time.time())
        random.shuffle(self.possible_posses)
        self.target = state

    def began(self):
        """
        Checks if the transition has begun.
        
        Returns:
            bool: True if the transition has begun, False otherwise.
        """
        return len(self.possible_posses) > 0 or len(self.cards) > 0

    def expand(self):
        """
        Expands the transition with a new card.
        
        Args:
            card: The card to add to the transition.
        """
        if not self.began():
            return
        
        if len(self.possible_posses) == 0:
            return

        random.seed(time.time())
        card = create_card()
        x, y = self.possible_posses.pop(0)
        self.cards.append((card, x + random.randint(-2, 2), y + random.randint(-1, 1)))

    def render(self, screen: Screen, term):
        """
        Renders the transition on the screen.
        
        Args:
            screen: The screen to render on.
            term: The terminal for styling.
        """
        if not self.complete and len(self.possible_posses) == 0:
            self.complete = True
            self.wrapper.set_state(self.target, force=True)

        for card, x, y in self.cards:
            if card.hidden:
                continue
            
            draw_card(term, screen, card, x, y)

