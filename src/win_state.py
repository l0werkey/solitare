from game_state import GameState
from pyfiglet import Figlet
import math
from core.enums import Difficulty
import random

class WinState(GameState):
    """
    Reprezentuje stan menu gry.
    
    Dziedziczy po GameState i implementuje metody specyficzne dla menu.
    """
    
    def __init__(self, id: str):
        super().__init__(id)

        self.x = 0
        self.x_off = 0

        self.particles = []
    
    def on_input(self, term, input) -> None:
        if int(self.x_off) <= 0:
            self.get_owner().menu()

    def init(self):
        self.x_off = self.get_owner()._screen.width

    def draw(self, term, screen):
        """
        Rysuje zawartość menu na ekranie.
        
        Args:
            term: Terminal do rysowania
            screen: Ekran, na którym rysujemy
        """
        if int(self.x_off) <= 0:
            screen.bg(term.on_black + " ")
        else:
            screen.bg(term.color(40) + " ")


        self.x += 1

        if self.x_off > 0:
            self.x_off -= 0.5
        elif self.x % 50 < 40:
            txt = "Press any key to continue"
            screen.insert_line(
                screen.width // 2 - len(txt) // 2,
                screen.height - 2,
                txt,
                prefix=term.bold + term.on_black + term.white,
                suffix=term.normal
            )

        if self.x % 5 == 0 and int(self.x_off) <= 0:
            self.particles.append([
                random.uniform(-0.5, 0.5),  # velocity
                [random.randint(0, screen.width - 1), -1],  # position
                term.color(random.randint(40, 255))  # color
            ])

        for particle in self.particles:
            particle[1][1] += 0.2
            particle[1][0] += particle[0]
            if particle[1][1] < 0 or particle[1][0] < 0 or particle[1][0] >= screen.width:
                if particle[1][1] > screen.height:
                    self.particles.remove(particle)
            else:
                screen.set_char(int(particle[1][0]), int(particle[1][1]), term.on_black + particle[2] + "*" + term.normal)
            particle[0] += (random.uniform(-0.5, 0.5) - particle[0]) / 10
                

        text = "YOU WIN!"
        f = Figlet(font='slant')
        full_width = len(f.renderText(text).splitlines()[0])
        for xp, char in enumerate(text):
            if char == " ":
                continue
            gened = f.renderText(char)
            for y, line in enumerate(gened.splitlines()):
                y_offset = int(math.sin(self.x / 10 + xp / 2) * 6)
                col = term.red
                if int(self.x/4)%len(text) == xp:
                    col = term.yellow
                bg_col = term.on_black if int(self.x_off) <= 0 else term.color(40)
                screen.insert_line(
                    xp*(full_width//len(text) + 8) + screen.width // 2 - full_width // 2 - 28 + int(self.x_off),
                    y + screen.height // 2 - len(gened.splitlines()) // 2 + y_offset,
                    line,
                    prefix=term.bold + bg_col + col,
                    suffix=term.normal
                )
