from enums import Difficulty
    
def get_draw_amount(difficulty: Difficulty) -> int:
    return 3 if difficulty == Difficulty.HARD else 1
