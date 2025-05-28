"""
Główny plik aplikacji - gra Pasjans w terminalu.
Zawiera punkt wejścia do programu i inicjalizację głównych komponentów gry.
"""

from game_wrapper import GameWrapper
from play_state import PlayState
# from menu_state import MenuState
from core.enums import Difficulty

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

    # play_state = MenuState("play_state")
    
    # game_wrapper.set_state(play_state)

    print("Wybierz poziom trudności:")
    print("1. Łatwy")
    print("2. Trudny")
    dif = None
    while True:
        choice = input("Wprowadź 1 lub 2: ")
        if choice == '1':
            dif = Difficulty.EASY
            break
        elif choice == '2':
            dif = Difficulty.HARD
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

    play_state = PlayState("play_state", difficulty=dif)
    game_wrapper.set_state(play_state)
    
    try:
        game_wrapper.run()
    except KeyboardInterrupt:
        game_wrapper.running = False
        print("Game interrupted. Exiting...")

if __name__ == "__main__":
    main()