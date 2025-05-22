from card import Card

class PilePart:
    def __init__(self, card: Card, next: 'PilePart' = None):
        self._card = card
        self._next = next

    def get_card(self) -> Card:
        return self._card

    def get_next(self) -> 'PilePart':
        return self._next