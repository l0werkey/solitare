from game_state import GameState

class MenuState(GameState):
    """
    Reprezentuje stan menu gry.
    
    Dziedziczy po GameState i implementuje metody specyficzne dla menu.
    """
    
    def __init__(self, id: str):
        super().__init__(id)
        self.options = ["Start Easy Game", "Start Hard Game"]
        self.option = 0
    
    def on_input(self, term, input) -> None:
        if input == term.KEY_UP or input == term.KEY_DOWN:
            if self.option == 0:
                self.option = 1
            else:
                self.option = 0
        pass
    
    def draw(self, term, screen):
        """
        Rysuje zawartość menu na ekranie.
        
        Args:
            term: Terminal do rysowania
            screen: Ekran, na którym rysujemy
        """
        screen.bg(term.on_black + " " + term.normal)

        screen.insert_line(screen.width // 2 - len("PASJANS") // 2, 1, "PASJANS", prefix=term.bold + term.white, suffix=term.normal)
        
        for i, option in enumerate(self.options):
            prefix = term.bold + term.white if i == self.option else term.normal
            text = option.upper() if i == self.option else option
            if i == self.option:
                text = "> " + text + " <"
            screen.insert_line(screen.width // 2 - len(text) // 2, 3 + i, text, prefix=prefix, suffix=term.normal)