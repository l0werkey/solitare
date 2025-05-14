import random
from card import Card
from enums import Suit, Rank
from difficulty import Difficulty, get_draw_amount

class Deck:
    def __init__(self):
        self.cards = []
        self.bank = []

        self.create_deck()
        self.shuffle_deck()

    def create_deck(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_cards(self, difficulty: Difficulty = Difficulty.HARD):
        amount = get_draw_amount(difficulty)

        drawn_cards = self.cards[:amount]
        self.cards = self.cards[amount:]
        self.bank.extend(drawn_cards)

        return drawn_cards
    
    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
            self.bank.append(card)
        elif card in self.bank:
            self.bank.remove(card)

    def remove_random_card(self):
        if not self.cards:
            return None
        random_card = random.choice(self.cards)
        self.remove_card(random_card)
        return random_card

    def is_deck_empty(self):
        return len(self.cards) == 0
    
    def refill_deck(self):
        self.cards.extend(self.bank)
        self.bank.clear()

    
