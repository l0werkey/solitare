from core.pile_part import PilePart, create_pile
from core.card import Card
from core.enums import Rank, TransferType
from typing import Optional, List, Union

class Tableau:
    PILE_COUNT = 7
    
    def __init__(self):
        self.piles = [None] * self.PILE_COUNT

    def _is_valid_index(self, idx: int) -> bool:
        return 0 <= idx < self.PILE_COUNT
    
    def get_pile(self, idx: int) -> Optional[PilePart]:
        if self._is_valid_index(idx):
            return self.piles[idx]
        return None
    
    def _is_valid_sequence_pair(self, card1: Card, card2: Card) -> bool:
        return (card1.rank.value == card2.rank.value + 1 and 
                not card1.is_same_color(card2))
        
    def can_place_card(self, card: Card, idx: int) -> bool:
        if not self._is_valid_index(idx):
            return False
            
        pile = self.piles[idx]
        if not pile:
            return card.rank == Rank.KING
            
        top = pile.get_last().get_card()
        return self._is_valid_sequence_pair(top, card)
        
    def _get_card_at_depth(self, idx: int, depth: int) -> Optional[PilePart]:
        pile = self.get_pile(idx)
        if not pile:
            return None
        return pile.get_at_depth(depth)
        
    def can_move_sequence(self, idx: int, depth: int) -> bool:
        current = self._get_card_at_depth(idx, depth)
        if not current:
            return False
            
        if not current.next:
            return True
            
        return self._is_valid_sequence(current)
    
    def can_place_sequence(self, start_part: PilePart, to_idx: int) -> bool:
        if not self._is_valid_index(to_idx):
            return False
            
        if not start_part or not start_part.next:
            return False
            
        if not self._is_valid_sequence(start_part):
            return False
            
        return self._can_place_on_destination(start_part.get_card(), to_idx)
    
    def _is_valid_sequence(self, start_part: PilePart) -> bool:
        current = start_part
        while current.next:
            card1 = current.get_card()
            card2 = current.next.get_card()
            
            if not self._is_valid_sequence_pair(card1, card2):
                return False
                
            current = current.next
            
        return True

    def _can_place_on_destination(self, card: Card, to_idx: int) -> bool:
        to_pile = self.piles[to_idx]
        
        if not to_pile:
            return card.rank == Rank.KING
        else:
            destination_card = to_pile.get_last().get_card()
            return self._is_valid_sequence_pair(destination_card, card)
    
    def _detach_from_source(self, from_idx: int, depth: int) -> None:
        if depth == 0:
            self.piles[from_idx] = None
        else:
            self.piles[from_idx].get_at_depth(depth - 1).next = None
    
    def _attach_to_destination(self, cards_to_move: PilePart, to_idx: int) -> None:
        to_pile = self.piles[to_idx]
        
        if not to_pile:
            self.piles[to_idx] = cards_to_move
        else:
            to_pile.get_last().next = cards_to_move

    def move_pile(self, from_idx: int, to_idx: int, depth: int) -> bool:
        if not self._is_valid_index(from_idx) or not self._is_valid_index(to_idx):
            return False
            
        if from_idx == to_idx or not self.piles[from_idx]:
            return False
        
        cards_to_move = self._get_card_at_depth(from_idx, depth)
        if not cards_to_move or not self.can_move_sequence(from_idx, depth):
            return False
        
        if not self._can_place_on_destination(cards_to_move.get_card(), to_idx):
            return False
        
        self._detach_from_source(from_idx, depth)
        self._attach_to_destination(cards_to_move, to_idx)
        
        # Reveal the new top card in the source pile if it exists and is hidden
        self._reveal_top_card(from_idx)
            
        return True

    def place_card(self, card: Card, idx: int) -> bool:
        if not self.can_place_card(card, idx):
            return False
            
        if not self.piles[idx]:
            self.piles[idx] = create_pile(card)
        else:
            self.piles[idx].add_card(card)
            
        return True

    def _get_second_to_last(self, pile: PilePart) -> Optional[PilePart]:
        if not pile.next:
            return None
            
        current = pile
        while current.next.next:
            current = current.next
            
        return current

    def remove_top_card(self, idx: int) -> Optional[Card]:
        if not self._is_valid_index(idx) or not self.piles[idx]:
            return None
            
        pile = self.piles[idx]
        
        if not pile.next:
            card = pile.get_card()
            self.piles[idx] = None
            return card
        
        second_to_last = self._get_second_to_last(pile)
        card = second_to_last.next.get_card()
        second_to_last.next = None
        
        self._reveal_top_card(idx)
        
        return card

    def get_top_card(self, idx: int) -> Optional[Card]:
        pile = self.get_pile(idx)
        if pile:
            return pile.get_last().get_card()
        return None

    def is_pile_empty(self, idx: int) -> bool:
        return self._is_valid_index(idx) and not self.piles[idx]

    def get_pile_size(self, idx: int) -> int:
        pile = self.get_pile(idx)
        if not pile:
            return 0
            
        return self._count_cards_in_pile(pile)
    
    def _count_cards_in_pile(self, pile: PilePart) -> int:
        count = 1
        current = pile
        while current.next:
            count += 1
            current = current.next
            
        return count
    
    def _reveal_top_card(self, idx: int) -> None:
        if not self._is_valid_index(idx):
            return
            
        pile = self.get_pile(idx)
        if pile:
            top_card = pile.get_last().get_card()
            if top_card.hidden:
                top_card.hidden = False
                
    def reveal_top_card_if_hidden(self, idx: int) -> None:
        self._reveal_top_card(idx)
    
    def get_type():
        return TransferType.TABLEAU
    
    def remove_pile(self, idx: int) -> bool:
        if not self._is_valid_index(idx):
            return False
        self.piles[idx] = None
        return True
    
    def copy(self) -> 'Tableau':
        new_tableau = Tableau()
        for i in range(self.PILE_COUNT):
            if self.piles[i]:
                new_tableau.piles[i] = self.piles[i].copy()
        return new_tableau