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
        py.draw_text(self.text, self.x, self.y, 20, py.WHITE)

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
        self.start_button = Button((100, 200), (100, 30), py.BLACK, py.GREEN, "Start")
        self.connect_button = Button((100, 300), (100, 30), py.BLACK, py.GREEN, "Connect")

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
        py.draw_text(self.name, 100, 200, 30, py.WHITE)

    def update(self) -> str:
        pressed = py.get_char_pressed()

        if 32 <= pressed <= 125 and len(self.name ) < 12:
            self.name += chr(pressed)

        if py.is_key_pressed(py.KeyboardKey.KEY_BACKSPACE):
            self.name = self.name[:-1]

        if py.is_key_pressed(py.KeyboardKey.KEY_ENTER):
            return "menu_main"

        return "NONE"
