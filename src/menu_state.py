from game_state import GameState
from pyfiglet import Figlet
import math
from play_state import PlayState
from core.enums import Difficulty
import random

class MenuState(GameState):
    """
    Reprezentuje stan menu gry.
    
    Dziedziczy po GameState i implementuje metody specyficzne dla menu.
    """
    
    def __init__(self, id: str):
        super().__init__(id)
        self.options = ["Start Easy Game", "Start Hard Game"]
        self.option = 0

        self.logo_offset = 0
        self.target_offset = 0

        self.intro = 0
        self.intro_target = 0
    
    def on_input(self, term, input) -> None:
        if int(self.intro) != self.intro_target:
            return
        if (input.name == "KEY_UP" or input.name == "KEY_LEFT") and self.option > 0:
            self.option -= 1
            self.target_offset += term.width
        elif (input.name == "KEY_DOWN" or input.name == "KEY_RIGHT") and self.option < len(self.options) - 1:
            self.option += 1
            self.target_offset -= term.width

        if input.name == "KEY_ENTER" or input.name == "KEY_RETURN":
            if self.option == 0:
                self.get_owner().reset_game(difficulty="easy")
                self.get_owner().set_state(PlayState("play_state", difficulty=Difficulty.EASY))
            elif self.option == 1:
                self.get_owner().reset_game(difficulty="hard")
                self.get_owner().set_state(PlayState("play_state", difficulty=Difficulty.HARD))
            elif self.option == 2:
                if self.get_owner().was_game_saved():
                    self.get_owner().load_game()
                    self.get_owner().set_state(PlayState("play_state", difficulty=self.get_owner().get_game().difficulty))


    def init(self):
        self.intro = self.get_owner()._term.height

        # if self.get_owner().was_game_saved():
        #     self.options.append("Continue")

    def render_logo(self, screen, term, color, motto="", x_offset=0, y_offset=0):
        text = "PASJANS"
        f = Figlet(font='slant')
        formated = f.renderText(text)
        first_len = len(formated.splitlines()[0]) + 4
        screen.insert_line(x_offset + screen.width // 2 - first_len // 2, y_offset, "╭" + "─" * (first_len - 2) + "╮", prefix=term.bold + color + term.white, suffix=term.normal)
        for y, line in enumerate(formated.splitlines()):
            line = f"│ {line} │"
            screen.insert_line(x_offset + screen.width // 2 - len(line) // 2, y + y_offset + 1, line, prefix=term.bold + color + term.white, suffix=term.normal)
        if motto:
            motto = motto.center(first_len - 2)
            screen.insert_line(x_offset + screen.width // 2 - len(motto) // 2 - 1, y + y_offset + 1, f"│{motto}│", prefix=term.bold + color + term.white, suffix=term.normal)
        screen.insert_line(x_offset + screen.width // 2 - first_len // 2, y + y_offset + 2, "╰" + "─" * (first_len - 2) + "╯", prefix=term.bold + color + term.white, suffix=term.normal)


    def draw(self, term, screen):
        """
        Rysuje zawartość menu na ekranie.
        
        Args:
            term: Terminal do rysowania
            screen: Ekran, na którym rysujemy
        """
        screen.bg(term.on_darkgreen + " " + term.normal)

        for i in range(100):
            random.seed(i)
            max_w = term.width
            max_h = term.height

            x = random.randint(0, max_w - 1)
            y = random.randint(0, max_h - 1)

            screen.set_char(x, y, term.on_darkgreen + term.green + "~" + term.normal)

        # ╭─────────╮
        # │ ?     - │
        # │         │
        # │ (? o ?) │
        # │         │
        # │ -     ? │
        # ╰─────────╯

        if int(self.intro) == self.intro_target:

            self.logo_offset += (self.target_offset - self.logo_offset) / 4
            
            self.render_logo(screen, term, term.on_color(18), x_offset=math.floor(self.logo_offset), y_offset=4, motto="Easy Mode")
            self.render_logo(screen, term, term.on_color(88), x_offset=math.floor(self.logo_offset)+term.width, y_offset=4, motto="Hard Mode")
            self.render_logo(screen, term, term.on_black, x_offset=math.floor(self.logo_offset)+term.width*2, y_offset=4, motto="Continue")

            for i, option in enumerate(self.options):
                prefix = term.bold + term.white + term.on_green if i == self.option else term.normal
                text = option.upper() if i == self.option else option
                if i == self.option:
                    text = "> " + text + " <"
                else:
                    text = "  " + text + "  "
                screen.insert_line(screen.width // 2 - len(text) // 2, 14 + i, text, prefix=prefix, suffix=term.normal)
        else:
            self.render_logo(screen, term, term.on_color(18), x_offset=math.floor(self.logo_offset), y_offset=4 + int(self.intro))
            self.intro += (self.intro_target - self.intro) / 6