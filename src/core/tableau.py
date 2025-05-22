from pile_part import PilePart

class Tableau:
    def __init__(self):
        self.piles: list[PilePart or None] = [None] * 7

    def move_pile(self, from_idx: int, to_idx: int, depth: int):
        pile_from = self.piles[from_idx]
        pile_to = self.piles[to_idx]

        cards_grabbed = pile_from.get_at_depth(depth)
        if cards_grabbed is None:
            return False

        placing_with = cards_grabbed.get_card()
        placing_on = pile_to.get_last().get_card()
        if pile_to.get_last() is not None:
            if placing_with.is_rank_higher(placing_on):
                return False
        else:
            pile_to.get_last().next = cards_grabbed