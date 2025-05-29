"""
Główny plik aplikacji - gra Pasjans w terminalu.
Zawiera punkt wejścia do programu i inicjalizację głównych komponentów gry.
"""

from game_wrapper import GameWrapper
from play_state import PlayState
from menu_state import MenuState
from core.enums import Difficulty
from win_state import WinState

def main():
    """
    Główna funkcja uruchamiająca grę.
    
    Tworzy instancję GameWrapper i PlayState, następnie uruchamia główną pętlę gry.
    Obsługuje przerwanie gry za pomocą Ctrl+C.
    """
    game_wrapper = GameWrapper()

    if game_wrapper._term.width < 120 or game_wrapper._term.height < 24:
        print("Terminal size is too small. Please use at least 80x24 terminal size.")
        return

    play_state = MenuState("menu_state")
    
    game_wrapper.set_state(play_state, force=True)
    
    try:
        game_wrapper.run()
    except KeyboardInterrupt:
        game_wrapper.running = False
        print("Game interrupted. Exiting...")

if __name__ == "__main__":
    main()