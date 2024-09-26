import pyray as py

class Element():
    def __init__(self, pos: tuple, size: tuple, color: py.Color, sec_color: py.Color) -> None:
        self.x = pos[0]
        self.y = pos[1]

        self.width = size[0]
        self.height = size[1]

        self.color = color
        self.sec_color = sec_color

        self.debug = False

    def render(self) -> None:
        if self.debug:
            py.draw_rectangle(self.x, self.y, self.width, self.height, py.RED)

class Button(Element):
    def __init__(self, pos: tuple, size: tuple, color: py.Color, sec_color: py.Color, text: str) -> None:
        super().__init__(pos, size, color, sec_color)

        self.text = text

        self.hover = False
        self.border = 5
        self.roundness = 0.6

    def render(self) -> None:
        if self.hover:
            py.draw_rectangle_rounded(py.Rectangle(self.x-self.border, self.y-self.border, self.width+self.border*2, self.height+self.border*2), self.roundness, 20, self.sec_color)

        py.draw_rectangle_rounded(py.Rectangle(self.x, self.y, self.width, self.height), self.roundness, 20, self.color)

        text_size = py.measure_text_ex(py.get_font_default(), self.text, 20, 1)
        py.draw_text(self.text, int(self.x + self.width / 2 - text_size.x / 2), int(self.y + self.height / 2 - text_size.y / 2), 20, py.RAYWHITE)

        super().render()

    def update(self) -> bool:
        mouse_pos = py.get_mouse_position()

        self.hover = False
        if py.check_collision_point_rec(mouse_pos, py.Rectangle(self.x, self.y, self.width, self.height)):
            self.hover = True

            if py.is_mouse_button_released(py.MouseButton.MOUSE_BUTTON_LEFT):
                return True

        if py.is_mouse_button_down(py.MouseButton.MOUSE_BUTTON_LEFT):
            self.hover = False

        return False

class Main():
    def __init__(self) -> None:
        self.start_button = Button((100, 200), (100, 30), py.DARKGRAY, py.GREEN, "Start")
        self.connect_button = Button((100, 300), (100, 30), py.DARKGRAY, py.GREEN, "Connect")

    def render(self) -> None:
        self.start_button.render()
        self.connect_button.render()

    def update(self) -> str:
        if self.start_button.update():
            return "create"
        
        if self.connect_button.update():
            return "connect"

        return "NONE"
    
class NewAcc():
    def __init__(self) -> None:
        self.name = ""

    def render(self) -> None:
        py.draw_text(self.name, 100, 200, 30, py.RAYWHITE)

    def update(self) -> str:
        pressed = py.get_char_pressed()

        if 32 <= pressed <= 125 and len(self.name) < 12:
            self.name += chr(pressed)

        if py.is_key_pressed(py.KeyboardKey.KEY_BACKSPACE):
            self.name = self.name[:-1]

        if py.is_key_pressed(py.KeyboardKey.KEY_ENTER):
            return "menu_main"

        return "NONE"
    
class ConnectToIn():
    def __init__(self) -> None:
        self.ip_port = ""

    def render(self) -> None:
        py.draw_text(self.ip_port, 50, 200, 20, py.RAYWHITE)

    def update(self) -> str:
        pressed = py.get_char_pressed()

        if 32 <= pressed <= 125 and len(self.ip_port) < 32:
            self.ip_port += chr(pressed)
            self.ip_port = self.ip_port.strip()

        if py.is_key_pressed(py.KeyboardKey.KEY_BACKSPACE):
            self.ip_port = self.ip_port[:-1]

        if py.is_key_pressed(py.KeyboardKey.KEY_ENTER):
            self.ip_port = self.ip_port.strip()
            return "connect_2"
        
        if py.is_key_down(py.KeyboardKey.KEY_LEFT_CONTROL):
            if py.is_key_pressed(py.KeyboardKey.KEY_V):
                self.ip_port += py.get_clipboard_text()

        return "NONE"
