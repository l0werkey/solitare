from card import Card

class PilePart:
    def __init__(self, card: Card, next: 'PilePart' = None):
        self._card = card
        self.next = next

    def get_card(self) -> Card:
        return self._card

    def add_card(self, card: Card):
        last = self.get_last()
        last.next = PilePart(card)

    def get_at_depth(self, depth: int) -> 'PilePart' or None:
        current = self
        for _ in range(depth):
            if current is None:
                return None
            current = current.next
        return current

    def get_last(self) -> 'PilePart':
        current = self
        while current.next is not None:
            current = current.next
        return current

def create_pile(*args: Card) -> PilePart:
    if not args:
        return None
    head = PilePart(args[0])
    current = head
    for card in args[1:]:
        current.next = PilePart(card)
        current = current.next
    return head