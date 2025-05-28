"""
Implementacja struktury danych dla reprezentacji stosu kart jako listy powiązanej.
Każdy PilePart reprezentuje jeden element w stosie kart.
"""

from core.card import Card

class PilePart:
    """
    Reprezentuje pojedynczy element w stosie kart zaimplementowanym jako lista powiązana.
    
    Każdy PilePart zawiera kartę i referencję do następnego elementu w stosie.
    Zapewnia funkcjonalność do manipulacji i przeszukiwania stosu kart.
    """
    
    def __init__(self, card: Card, next: 'PilePart' = None):
        """
        Inicjalizuje nowy element stosu kart.
        
        Args:
            card (Card): Karta przypisana do tego elementu
            next (PilePart, optional): Następny element w stosie
        """
        self._card = card
        self.next = next

    def get_card(self) -> Card:
        """
        Zwraca kartę przypisaną do tego elementu.
        
        Returns:
            Card: Karta w tym elemencie stosu
        """
        return self._card

    def add_card(self, card: Card):
        """
        Dodaje nową kartę na koniec stosu.
        
        Args:
            card (Card): Karta do dodania na koniec stosu
        """
        last = self.get_last()
        last.next = PilePart(card)

    def get_at_depth(self, depth: int) -> 'PilePart | None':
        """
        Zwraca element stosu na określonej głębokości.
        
        Args:
            depth (int): Głębokość elementu (0 = pierwszy element)
            
        Returns:
            PilePart | None: Element na określonej głębokości lub None
        """
        current = self
        for _ in range(depth):
            if current is None:
                return None
            current = current.next
        return current

    def get_last(self) -> 'PilePart':
        """
        Zwraca ostatni element w stosie.
        
        Returns:
            PilePart: Ostatni element w stosie
        """
        current = self
        while current.next is not None:
            current = current.next
        return current
    
    def is_last(self) -> bool:
        """
        Sprawdza czy ten element jest ostatni w stosie.
        
        Returns:
            bool: True jeśli to ostatni element
        """
        return self.next is None
    
    def length(self) -> int:
        """
        Zwraca liczbę elementów w stosie począwszy od tego elementu.
        
        Returns:
            int: Liczba elementów w stosie
        """
        count = 0
        current = self
        while current is not None:
            count += 1
            current = current.next
        return count
    
    def is_sorted(self, reversed=False) -> bool:
        """
        Sprawdza czy karty w stosie są posortowane według rangi.
        
        Args:
            reversed (bool): True dla sortowania malejącego, False dla rosnącego
            
        Returns:
            bool: True jeśli karty są posortowane
        """
        current = self
        previous_rank = None
        while current is not None:
            if previous_rank is not None:
                if reversed:
                    if current.get_card().rank.value >= previous_rank.value:
                        return False
                else:
                    if current.get_card().rank.value <= previous_rank.value:
                        return False
            previous_rank = current.get_card().rank
            current = current.next
        return True
    
    def as_list(self) -> list[Card]:
        cards = []
        current = self
        while current is not None:
            cards.append(current.get_card())
            current = current.next
        return cards
    
    def is_hidden(self) -> bool:
        current = self
        while current is not None:
            if current.get_card().hidden:
                return True
            current = current.next
        return False
    
    def copy(self):
        if self is None:
            return None
        new_head = PilePart(self.get_card().copy())
        current_new = new_head
        current_old = self.next
        while current_old is not None:
            current_new.next = PilePart(current_old.get_card().copy())
            current_new = current_new.next
            current_old = current_old.next
        return new_head

def create_pile(*args: Card) -> PilePart:
    if not args:
        return None
    head = PilePart(args[0])
    current = head
    for card in args[1:]:
        current.next = PilePart(card)
        current = current.next
    return head