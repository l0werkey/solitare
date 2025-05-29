from core.card import Card
from core.enums import TransferContext, TransferType, Difficulty
from core.pile_part import PilePart
from typing import Optional, Union, Callable
from core.stock import Stock
from core.foundations import Foundations
from core.tableau import Tableau

class Offer:
    def __init__(self, item: Optional[Union[Card, PilePart]], complete_offer: Callable[[], None]):
        self.item = item
        self.complete_offer = complete_offer
        self.signature = None

    def complete(self):
        self.complete_offer()
        if self.signature:
            self.signature(self)
    
    def sign(self, signature: Callable[['Offer'], None]):
        self.signature = signature

class Transfer:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
    
    def create_offer(self, offering_to: TransferType) -> Optional[Offer]:
        return None
    
    def complete_offer(self):
        return None
    
    def verify_offer(self, offer: Offer) -> bool:
        return False
    
class TableauTransfer(Transfer):
    def __init__(self, tableau: Tableau, source_index: int, depth: int = 0, difficulty: Difficulty = Difficulty.HARD):
        super().__init__(difficulty)
        self.tableau = tableau
        self.source_index = source_index
        self.depth = depth

    def get_type(self) -> TransferType:
        return TransferType.TABLEAU

    def create_offer(self, offering_to: TransferType) -> Optional[Offer]:
        # check if the card is last
        source_pile = self.tableau.get_pile(self.source_index)
        if source_pile is None:
            return None
        
        if source_pile.get_at_depth(self.depth) is None:
            return None
        
        sub_pile = source_pile.get_at_depth(self.depth)
        if sub_pile is None:
            return None
        
        if sub_pile.is_last():
            return Offer(
                item=sub_pile.get_card(),
                complete_offer=self.complete_offer
            )
        else:
            return Offer(
                item=sub_pile,
                complete_offer=self.complete_offer
            )
        
    def complete_offer(self):
        pile = self.tableau.get_pile(self.source_index)
        if pile is None:
            return
        
        if self.depth == 0:
            self.tableau.remove_pile(self.source_index)
            return

        sub_pile_parent = pile.get_at_depth(self.depth - 1) if self.depth > 0 else None
        if sub_pile_parent is None:
            return
        
        sub_pile_parent.next = None
        
        # Reveal the new top card if it's hidden
        self.tableau.reveal_top_card_if_hidden(self.source_index)

    def verify_offer(self, offer: Offer) -> bool:
        if not offer or not offer.item:
            return False
        
        if isinstance(offer.item, Card):
            if self.tableau.can_place_card(offer.item, self.source_index):
                offer.sign(self.create_signature())
                return True
        elif isinstance(offer.item, PilePart):
            if self.tableau.can_place_sequence(offer.item, self.source_index):
                offer.sign(self.create_signature())
                return True
        return False
    
    def create_signature(self) -> Optional[Callable[['Offer'], None]]:
        def signature(offer: Offer):
            if isinstance(offer.item, Card):
                self.tableau.place_card(offer.item, self.source_index)
            elif isinstance(offer.item, PilePart):
                last_card = self.tableau.get_pile(self.source_index).get_last()
                last_card.next = offer.item

        return signature
    
class StockTransfer(Transfer):
    def __init__(self, stock: Stock, difficulty: Difficulty = Difficulty.HARD):
        super().__init__(difficulty)
        self.stock = stock

    def get_type(self) -> TransferType:
        return TransferType.STOCK

    def create_offer(self, offering_to: TransferType) -> Optional[Offer]:
        if not self.stock.can_draw_from_waste(self.difficulty):
            return None

        card = self.stock.get_top_waste_card()
        if not card:
            return None

        return Offer(
            item=card,
            complete_offer=self.complete_offer
        )
    
    def complete_offer(self):
        self.stock.draw_top_card_from_waste()
    
    def verify_offer(self, offer: Offer) -> bool: # Can't move to stock - thus do not verify
        return False

class FoundationTransfer(Transfer):
    def __init__(self, foundations: Foundations, target_index: int, difficulty: Difficulty = Difficulty.HARD):
        super().__init__(difficulty)
        self.foundations = foundations
        self.target_index = target_index

    def get_type(self) -> TransferType:
        return TransferType.FOUNDATION

    def create_offer(self, offering_to: TransferType) -> Optional[Offer]:
        if not self.foundations.can_place_card(self.target_index):
            return None
        
        card = self.foundations.get_top_card(self.target_index)
        if card is None:
            return None
        
        return Offer(
            item=card,
            complete_offer=self.complete_offer
        )
    
    def complete_offer(self):
        self.foundations.place_top_card(self.target_index)
    
    def verify_offer(self, offer: Offer) -> bool:
        if not offer or not offer.item:
            return False
        
        if isinstance(offer.item, Card):
            if self.foundations.can_place_card(offer.item):
                offer.sign(self.create_signature())
                return True
        return False
    
    def create_signature(self) -> Optional[Callable[['Offer'], None]]:
        def signature(offer: Offer):
            self.foundations.place_card(offer.item)
        
        return signature
