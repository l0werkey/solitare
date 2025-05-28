from blessed import Terminal
import sys
import time

term = Terminal()

class UndoRedoManager:
    def __init__(self, max_history=50):
        self.history = []  # List of Art state snapshots
        self.current_index = -1  # -1 means no history, 0+ means position in history
        self.max_history = max_history
    
    def save_state(self, art):
        state = {
            'width': art.width,
            'height': art.height,
            'chars': [row[:] for row in art.chars]  # Deep copy of 2D array
        }
        
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        self.history.append(state)
        self.current_index = len(self.history) - 1
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index = len(self.history) - 1
    
    def undo(self, art):
        if self.can_undo():
            self.current_index -= 1
            state = self.history[self.current_index]
            self._restore_state(art, state)
            return True
        return False
    
    def redo(self, art):
        if self.can_redo():
            self.current_index += 1
            state = self.history[self.current_index]
            self._restore_state(art, state)
            return True
        return False
    
    def _restore_state(self, art, state):
        art.width = state['width']
        art.height = state['height']
        art.chars = [row[:] for row in state['chars']]  # Deep copy
    
    def can_undo(self):
        return self.current_index > 0
    
    def can_redo(self):
        return self.current_index < len(self.history) - 1

class ToastManager:
    def __init__(self, max_toasts=3, duration=4.0):
        self.toasts = []  # List of (message, timestamp) tuples
        self.max_toasts = max_toasts
        self.duration = duration
    
    def add_toast(self, message):
        current_time = time.time()
        self.toasts.append((message, current_time))
        
        # Keep only the most recent toasts
        if len(self.toasts) > self.max_toasts:
            self.toasts = self.toasts[-self.max_toasts:]
    
    def get_active_toasts(self):
        current_time = time.time()
        active_toasts = []
        
        for message, timestamp in self.toasts:
            if current_time - timestamp < self.duration:
                active_toasts.append(message)
        
        self.toasts = [(msg, ts) for msg, ts in self.toasts 
                       if current_time - ts < self.duration]
        
        return active_toasts
    
    def draw_toasts(self):
        active_toasts = self.get_active_toasts()
        
        for i in range(3):
            print(term.move_xy(0, i) + term.clear_eol, end='')
        
        for i, message in enumerate(active_toasts):
            if i < 3:  # Only show first 3 toasts
                print(term.move_xy(0, i) + message, end='')
        
        print('', end='', flush=True)

class Art:
    def __init__(self, initial_width: int = 0, initial_height: int = 0):
        self.width = initial_width
        self.height = initial_height
        self.chars = [[' ' for _ in range(initial_width)] for _ in range(initial_height)]
    
    def modify_size(self, left_expansion: int = 0, right_expansion: int = 0, top_expansion: int = 0, bottom_expansion: int = 0):
        new_width = self.width + left_expansion + right_expansion
        new_height = self.height + top_expansion + bottom_expansion
        
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        shift_x = left_expansion
        shift_y = top_expansion

        new_chars = [[' ' for _ in range(new_width)] for _ in range(new_height)]
        
        for y in range(self.height):
            for x in range(self.width):
                new_y = y + shift_y
                new_x = x + shift_x
                # Only copy if the destination is within the new bounds
                if 0 <= new_y < new_height and 0 <= new_x < new_width:
                    new_chars[new_y][new_x] = self.chars[y][x]
                    
        self.chars = new_chars
        self.width = new_width
        self.height = new_height

    def draw(self, x: int, y: int):
        for row in range(self.height):
            for col in range(self.width):
                print(term.move_xy(x + col, y + row) + self.chars[row][col], end='')
        print(term.normal, end='', flush=True)

def get_input(prompt):
    print(prompt, end='', flush=True)
    buffer = ""
    while True:
        key = term.inkey()
        if key.name == 'KEY_ENTER':
            break
        elif key.name == 'KEY_BACKSPACE':
            if buffer:
                buffer = buffer[:-1]
                print('\b \b', end='', flush=True)
        elif key.name == 'KEY_ESCAPE':
            return None  # User cancelled
        elif key.is_sequence:
            continue  # Ignore control sequences
        else:
            buffer += key
            print(key, end='', flush=True)
    print()
    return buffer

def get_width_height(prompt="Enter initial width and height (e.g., 80x25): "):
    with term.cbreak():
        buffer = get_input(prompt)
        if buffer is None:
            return None, None

    try:
        width_str, height_str = buffer.lower().split('x')
        width = int(width_str.strip())
        height = int(height_str.strip())
        return width, height
    except Exception as e:
        print(f"Invalid input: {e}")
        return None, None

def get_filename(prompt="Enter filename to save (or press ESC to cancel): "):
    with term.cbreak():
        return get_input(prompt)

def export_art(art, filename):
    try:
        # Add .txt extension if not present
        if not filename.lower().endswith('.txt'):
            filename += '.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            for row in art.chars:
                # Convert row to string, removing trailing spaces
                line = ''.join(row).rstrip()
                f.write(line + '\n')
        
        return True, f"Art exported to {filename}"
    except Exception as e:
        return False, f"Export failed: {e}"

def draw_border(top_left_x, top_left_y, width, height):
    top_left = '┌'
    top_right = '┐'
    bottom_left = '└'
    bottom_right = '┘'
    horizontal = '─'
    vertical = '│'
    
    for x in range(width + 2):
        for y in range(height + 2):
            char = ' '
            
            if x == 0 and y == 0:
                char = top_left
            elif x == width + 1 and y == 0:
                char = top_right
            elif x == 0 and y == height + 1:
                char = bottom_left
            elif x == width + 1 and y == height + 1:
                char = bottom_right
            elif y == 0 or y == height + 1:
                char = horizontal
            elif x == 0 or x == width + 1:
                char = vertical
            
            print(term.move_xy(top_left_x + x, top_left_y + y) + char, end='')
    
    print('', end='', flush=True)

def draw_cursor(top_left_x, top_left_y, cursor, visible, art=None):
    x, y = cursor
    # Check if cursor position is within bounds
    if art and (x < 0 or x >= art.width or y < 0 or y >= art.height):
        return  # Skip drawing if cursor is out of bounds
    
    if visible:
        ch = art.chars[y][x]
        print(term.move_xy(top_left_x + x + 1, top_left_y + y + 1) + term.reverse + ch + term.normal, end='', flush=True)
    else:
        if art:
            ch = art.chars[y][x]
            print(term.move_xy(top_left_x + x + 1, top_left_y + y + 1) + ch, end='', flush=True)
        else:
            print(term.move_xy(top_left_x + x + 1, top_left_y + y + 1) + ' ', end='', flush=True)

def move_cursor(cursor, direction, width, height):
    x, y = cursor
    if direction == 'up':
        y = (y - 1) % height
    elif direction == 'down':
        y = (y + 1) % height
    elif direction == 'left':
        x = (x - 1) % width
    elif direction == 'right':
        x = (x + 1) % width
    return (x, y)

def move_cursor_reverse(cursor, direction, width, height):
    reverse_directions = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }
    return move_cursor(cursor, reverse_directions[direction], width, height)

def clamp_cursor(cursor, width, height):
    x, y = cursor
    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))
    return (x, y)

def resize_by_bottom_right(art, width_change, height_change):
    # Ensure we don't shrink below 1x1
    if width_change < 0 and abs(width_change) >= art.width:
        width_change = -art.width + 1
    if height_change < 0 and abs(height_change) >= art.height:
        height_change = -art.height + 1

    art.modify_size(left_expansion=0, right_expansion=width_change, top_expansion=0, bottom_expansion=height_change)
    return art

def resize_by_top_left(art, width_change, height_change):
    # Ensure we don't shrink below 1x1
    if width_change < 0 and abs(width_change) >= art.width:
        width_change = -art.width + 1
    if height_change < 0 and abs(height_change) >= art.height:
        height_change = -art.height + 1

    art.modify_size(left_expansion=width_change, right_expansion=0, top_expansion=height_change, bottom_expansion=0)
    return art

def clear_area(x, y, width, height):
    for row in range(height + 2):
        print(term.move_xy(x, y + row) + ' ' * (width + 2), end='')

def redraw_canvas_and_border(cx, cy, art, toast_manager=None):
    # Clear the entire canvas area first
    clear_area(cx, cy, art.width, art.height)
    draw_border(cx, cy, art.width, art.height)
    art.draw(cx + 1, cy + 1)
    
    # Redraw toasts if manager is provided
    if toast_manager:
        toast_manager.draw_toasts()

def main():
    print("ASCII Art Maker")
    print("Controls:")
    print("- Arrow keys: Move cursor")
    print("- Shift+Arrow keys: Resize canvas")
    print("- Home: Toggle resize mode (bottom_right/top_left)")
    print("- Insert: Export to file")
    print("- Backspace: Erase and move reverse")
    print("- Ctrl+Z: Undo")
    print("- Ctrl+Y: Redo")
    print("- Type any character to draw")
    print("- Ctrl+C: Exit")
    print()
    
    initial_width, initial_height = get_width_height()
    if initial_width is None or initial_height is None:
        print("Exiting due to invalid input.")
        sys.exit(1)

    # Ensure minimum size
    initial_width = max(1, initial_width)
    initial_height = max(1, initial_height)

    art = Art(initial_width, initial_height)

    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear, end='', flush=True)

            toast_manager = ToastManager()
            undo_manager = UndoRedoManager()
            
            cx, cy = 2, 5
            
            undo_manager.save_state(art)
            
            redraw_canvas_and_border(cx, cy, art, toast_manager)

            cursor = (0, 0)
            cursor_visible = True
            cursor_direction = 'right'
            prev_cursor = cursor

            resize_mode = 'bottom_right'  # default resize mode
            
            toast_manager.add_toast(f"Resize mode: {resize_mode}")
            toast_manager.draw_toasts()

            while True:
                key = term.inkey(timeout=0.4)
                resized = False
                state_changed = False  # Track if we need to save state for undo

                if not key:
                    cursor_visible = not cursor_visible
                    toast_manager.draw_toasts()
                else:
                    cursor_visible = True

                    if key.name == 'KEY_SUP':
                        resized = True
                        state_changed = True
                        clear_area(cx, cy, art.width, art.height)
                        if resize_mode == 'bottom_right':
                            resize_by_bottom_right(art, 0, -1)
                        elif resize_mode == 'top_left':
                            resize_by_top_left(art, 0, -1)
                        toast_manager.add_toast(f"Canvas resized to {art.width}x{art.height}")
                    elif key.name == 'KEY_SDOWN':
                        resized = True
                        state_changed = True
                        clear_area(cx, cy, art.width, art.height)
                        if resize_mode == 'bottom_right':
                            resize_by_bottom_right(art, 0, 1)
                        elif resize_mode == 'top_left':
                            resize_by_top_left(art, 0, 1)
                        toast_manager.add_toast(f"Canvas resized to {art.width}x{art.height}")
                    elif key.name == 'KEY_SLEFT':
                        resized = True
                        state_changed = True
                        clear_area(cx, cy, art.width, art.height)
                        if resize_mode == 'bottom_right':
                            resize_by_bottom_right(art, -1, 0)
                        elif resize_mode == 'top_left':
                            resize_by_top_left(art, -1, 0)
                        toast_manager.add_toast(f"Canvas resized to {art.width}x{art.height}")
                    elif key.name == 'KEY_SRIGHT':
                        resized = True
                        state_changed = True
                        clear_area(cx, cy, art.width, art.height)
                        if resize_mode == 'bottom_right':
                            resize_by_bottom_right(art, 1, 0)
                        elif resize_mode == 'top_left':
                            resize_by_top_left(art, 1, 0)
                        toast_manager.add_toast(f"Canvas resized to {art.width}x{art.height}")

                    elif key.name == 'KEY_HOME':
                        if resize_mode == 'bottom_right':
                            resize_mode = 'top_left'
                        else:
                            resize_mode = 'bottom_right'
                        toast_manager.add_toast(f"Resize mode: {resize_mode}")
                    
                    elif key.name == 'KEY_INSERT':
                        toast_manager.add_toast("Enter filename to export...")
                        toast_manager.draw_toasts()
                        
                        filename = get_filename("Enter filename to save (or press ESC to cancel): ")
                        
                        if filename:
                            success, message = export_art(art, filename)
                            toast_manager.add_toast(message)
                        else:
                            toast_manager.add_toast("Export cancelled")
                        
                        redraw_canvas_and_border(cx, cy, art, toast_manager)

                    elif key.name == 'KEY_BACKSPACE':
                        new_cursor = move_cursor_reverse(cursor, cursor_direction, art.width, art.height)
                        x, y = new_cursor
                        if 0 <= x < art.width and 0 <= y < art.height:
                            if art.chars[y][x] != ' ':  # Only save state if there's something to erase
                                state_changed = True
                            art.chars[y][x] = ' '  # Erase character
                            cursor = new_cursor

                    elif key == '\x1a':  # Ctrl+Z (undo)
                        if undo_manager.undo(art):
                            toast_manager.add_toast("Undo")
                            cursor = clamp_cursor(cursor, art.width, art.height)
                            prev_cursor = clamp_cursor(prev_cursor, art.width, art.height)
                            redraw_canvas_and_border(cx, cy, art, toast_manager)
                        else:
                            toast_manager.add_toast("Nothing to undo")

                    elif key == '\x19':  # Ctrl+Y (redo)
                        if undo_manager.redo(art):
                            toast_manager.add_toast("Redo")
                            cursor = clamp_cursor(cursor, art.width, art.height)
                            prev_cursor = clamp_cursor(prev_cursor, art.width, art.height)
                            redraw_canvas_and_border(cx, cy, art, toast_manager)
                        else:
                            toast_manager.add_toast("Nothing to redo")

                    elif key.name == 'KEY_UP':
                        cursor = move_cursor(cursor, 'up', art.width, art.height)
                        cursor_direction = 'up'
                    elif key.name == 'KEY_DOWN':
                        cursor = move_cursor(cursor, 'down', art.width, art.height)
                        cursor_direction = 'down'
                    elif key.name == 'KEY_LEFT':
                        cursor = move_cursor(cursor, 'left', art.width, art.height)
                        cursor_direction = 'left'
                    elif key.name == 'KEY_RIGHT':
                        cursor = move_cursor(cursor, 'right', art.width, art.height)
                        cursor_direction = 'right'
                    else:
                        if key.isprintable():
                            x, y = cursor
                            if 0 <= x < art.width and 0 <= y < art.height:
                                if art.chars[y][x] != key:
                                    state_changed = True
                                art.chars[y][x] = key
                                cursor = move_cursor(cursor, cursor_direction, art.width, art.height)

                if state_changed:
                    undo_manager.save_state(art)

                if resized:
                    cursor = clamp_cursor(cursor, art.width, art.height)
                    prev_cursor = clamp_cursor(prev_cursor, art.width, art.height)
                    redraw_canvas_and_border(cx, cy, art, toast_manager)

                toast_manager.draw_toasts()

                draw_cursor(cx, cy, prev_cursor, False, art)
                draw_cursor(cx, cy, cursor, cursor_visible, art)

                prev_cursor = cursor

    except KeyboardInterrupt:
        print(term.normal + term.clear)
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()