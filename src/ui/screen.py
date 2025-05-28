import sys
from blessed import Terminal

class Screen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.chars = [[" " for _ in range(width)] for _ in range(height)]
        self.prev_chars = [row.copy() for row in self.chars]

        self.last_delta_num = 0

    def clear(self):
        self.chars = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def set_char(self, x: int, y: int, char: str):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.chars[y][x] = char

    def get_char(self, x: int, y: int) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.chars[y][x]
        return " "
    
    def insert_line(self, x: int, y: int, line: str, prefix="", suffix=""):
        if 0 <= y < self.height:
            for i, char in enumerate(line):
                cx = x + i
                if 0 <= cx < self.width:
                    self.chars[y][cx] = f"{prefix}{char}{suffix}"

    def bg(self, char: str):
        for y in range(self.height):
            for x in range(self.width):
                self.chars[y][x] = char

    def rect(self, x: int, y: int, width: int, height: int, char: str):
        for dy in range(height):
            for dx in range(width):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    self.chars[y + dy][x + dx] = char

    def line(self, x0: int, y0: int, x1: int, y1: int, char: str) -> None:
        steep = abs(y1 - y0) > abs(x1 - x0)
        
        if steep:
            x0, y0 = y0, x0  # swap(x0, y0)
            x1, y1 = y1, x1  # swap(x1, y1)
        
        if x0 > x1:
            x0, x1 = x1, x0  # swap(x0, x1)
            y0, y1 = y1, y0  # swap(y0, y1)
        
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2  # Integer division equivalent to dx / 2
        
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        
        x = x0
        while x <= x1:
            if steep:
                self.set_char(y0, x, char)  # drawPixel(y0, x, color)
            else:
                self.set_char(x, y0, char)  # drawPixel(x, y0, color)
            
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            
            x += 1



    def render(self, term: Terminal, x_pos: int = 0, y_pos: int = 0) -> None:
        deltas = [[self.chars[y][x] != self.prev_chars[y][x]
                   for x in range(self.width)]
                  for y in range(self.height)]

        self.last_delta_num = sum(sum(1 for cell in row if cell) for row in deltas)

        if self.last_delta_num > 0:
            sys.stdout.write(term.home)

            out = []
            for y in range(self.height):
                x = 0
                while x < self.width:
                    if deltas[y][x]:
                        start = x
                        buf = []
                        while x < self.width and deltas[y][x]:
                            buf.append(self.chars[y][x])
                            x += 1
                        out.append(term.move_xy(start + x_pos, y + y_pos))
                        out.append(''.join(buf))
                    else:
                        x += 1

            sys.stdout.write(''.join(out))
            sys.stdout.flush()

            self.prev_chars = [row.copy() for row in self.chars]
