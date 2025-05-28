from blessed import Terminal
from core.card import Card
from core.enums import Suit, Color, Rank
from ui.screen import Screen

# ╭─────────╮
# │ ?     - │
# │         │
# │ (? o ?) │
# │         │
# │ -     ? │
# ╰─────────╯

def rank_to_ascii(rank: Rank):
    match rank:
        case Rank.ACE:
            return [
                "  ┌───┐  ",
                "  ├───┤  ",
                "  │   │  ",
            ]
        case Rank.TWO:
            return [
                "  ────┐  ",
                "  ┌───┘  ",
                "  └────  "
            ]
        case Rank.THREE:
            return [
                "  ────┐  ",
                "  ────┤  ",
                "  ────┘  "
            ]
        case Rank.FOUR:
            return [
                "  │   │  ",
                "  └───┤  ",
                "      │  ",
            ]
        case Rank.FIVE:
            return [
                "  ┌────  ",
                "  └───┐  ",
                "  ────┘  "
            ]
        case Rank.SIX:
            return [
                "  ┌────  ",
                "  ├───┐  ",
                "  └───┘  "
            ]
        case Rank.SEVEN:
            return [
                "  ────┐  ",
                "     ╱   ",
                "    ╱    "
            ]
        case Rank.EIGHT:
            return [
                "  ┌───┐  ",
                "  ├───┤  ",
                "  └───┘  "
            ]
        case Rank.NINE:
            return [
                "  ┌───┐  ",
                "  └───┤  ",
                "  └───┘  "
            ]
        case Rank.TEN:
            return [
                "  ┐ ┌─┐  ",
                "  │ │ │  ",
                "  ┴ └─┘  "
            ]
        case Rank.JACK:
            return [
                "         ",
                " (' - ') ",
                "         "
            ]
        case Rank.QUEEN:
            return [
                "  (*^*)  ",
                " (^ 3 ^) ",
                "         "
            ]
        case Rank.KING:
            return [
                "  [^^^]  ",
                " (^ - ^) ",
                "         "
            ]
        case _:
            return [
                "         ",
                " (? o ?) ",
                "         "
            ]
        

def draw_card(term: Terminal, screen: Screen, card: Card, x: int, y: int, invert: bool = False):
    color = term.color(40) if card.get_color() == Color.BLACK else term.on_color(88)

    rank = card.rank.short_name() if not card.hidden else '???'
    while len(rank) < 3:
        rank += ' '

    if card.hidden:
        rank = "?  "
        color = term.on_color(18)

    reversed_rank = ''
    for char in rank:
        if char == ' ':
            reversed_rank = ' ' + reversed_rank
        else:
            reversed_rank = reversed_rank + char

    suit = card.suit if not card.hidden else '???'
    if card.hidden:
        suit = '-'

    ascii_center = rank_to_ascii(card.rank if not card.hidden else None)

    if invert:
        color = term.reverse + color

    screen.insert_line(x, y, '╭─────────╮', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 1, f'│ {rank}   {suit} │', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 2, f'│{ascii_center[0]}│', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 3, f'│{ascii_center[1]}│', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 4, f'│{ascii_center[2]}│', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 5, f'│ {suit}   {reversed_rank} │', prefix=color + term.white, suffix=term.normal)
    screen.insert_line(x, y + 6, '╰─────────╯', prefix=color + term.white, suffix=term.normal)


def draw_foundation_base(term: Terminal, screen: Screen, suit: Suit, x: int, y: int, invert: bool = False):
    color = term.on_black + term.white

    if invert:
        color = color = term.on_white + term.black

    screen.insert_line(x, y, '╭─────────╮', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 1, f'│       {suit} │', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 2, f'│         │', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 3, f'│         │', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 4, f'│         │', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 5, f'│ {suit}       │', prefix=color, suffix=term.normal)
    screen.insert_line(x, y + 6, '╰─────────╯', prefix=color, suffix=term.normal)

def draw_card_top(term: Terminal, screen: Screen, card: Card, x: int, y: int, invert: bool = False):
    color = term.color(40) if card.get_color() == Color.BLACK else term.on_color(88)

    rank = card.rank.short_name() if not card.hidden else '??'
    while len(rank) < 2:
        rank += ' '

    suit = card.suit if not card.hidden else '?'

    if card.hidden:
        rank = '??'
        suit = '?'
        color = term.on_color(18)

    if invert:
        color = term.reverse + color

    screen.insert_line(x, y, f'╭┉{rank}┉──┉{suit}┉╮', prefix=color + term.white, suffix=term.normal)