from enum import Enum, auto

class Difficulty(Enum):
    EASY = auto()
    HARD = auto()

    def __str__(self):
        return self.name.capitalize()
    
def get_draw_amount(difficulty: Difficulty) -> int:
    return 3 if difficulty == Difficulty.HARD else 1