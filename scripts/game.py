import pyray as py

from scripts.profile import Profile

TRUE_COLOR = py.Color(255, 0, 0, 255)
FALSE_COLOR = py.Color(0, 0, 255, 255)

TRUE_COLOR_A = py.Color(255, 0, 0, 100)
FALSE_COLOR_A = py.Color(0, 0, 255, 100)

class SmallCube():
    def __init__(self, x: int, y: int, px: int, py: int) -> None:
        self.x = x
        self.y = y

        self.px = px
        self.py = py

        self.color = None
        self.size_off = 10

    def render(self) -> None:
        if self.color != None:
            rect = py.Rectangle(self.px*201+self.x*67+self.size_off, self.py*201+self.y*67+self.size_off, 67-self.size_off*2, 67-self.size_off*2)
            if self.color == True:
                py.draw_rectangle_rounded(rect, 0.1, 20, TRUE_COLOR)

            else:
                py.draw_rectangle_rounded(rect, 0.1, 20, FALSE_COLOR)

class BigCube():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.won = None

        self.field = {}
        for x in range(3):
            for y in range(3):
                self.field.update({(x, y) : SmallCube(x, y, self.x, self.y)})

    def render(self) -> None:
        for item in self.field.values():
            item.render()

        if self.won:
            py.draw_rectangle_rounded(py.Rectangle(self.x*201, self.y*201, 201, 201), 0.05, 20, TRUE_COLOR_A)

        elif self.won == False:
            py.draw_rectangle_rounded(py.Rectangle(self.x*201, self.y*201, 201, 201), 0.05, 20, FALSE_COLOR_A)

    def check_win(self) -> bool:
        for col in range(3):
            if self.field[(col, 0)].color == self.field[(col, 1)].color == self.field[(col, 2)].color:
                if self.field[(col, 0)].color != None:
                    self.won = self.field[(col, 0)].color
                    return self.won

        for row in range(3):
            if self.field[(0, row)].color == self.field[(1, row)].color == self.field[(2, row)].color:
                if self.field[(0, row)].color != None:
                    self.won = self.field[(0, row)].color
                    return self.won

        if self.field[(0, 0)].color == self.field[(1, 1)].color == self.field[(2, 2)].color:
            if self.field[(0, 0)].color != None:
                self.won = self.field[(0, 0)].color
                return self.won

        if self.field[(2, 0)].color == self.field[(1, 1)].color == self.field[(0, 2)].color:
            if self.field[(2, 0)].color != None:
                self.won = self.field[(0, 2)].color
                return self.won

        return None

class Field():
    def __init__(self) -> None:
        self.field = {}
        self.won = None

        for x in range(3):
            for y in range(3):
                self.field.update({(x, y) : BigCube(x, y)})

    def render(self) -> None:
        for item in self.field.values():
            item.render()
            item.check_win()

    def set_cube(self, b_pos: tuple, s_pos: tuple, color: bool):
        self.field[b_pos].field[s_pos].color = color
        print(b_pos, s_pos, " PLACED")

    def check_win(self) -> bool:
        for col in range(3):
            if self.field[(col, 0)].won == self.field[(col, 1)].won == self.field[(col, 2)].won:
                if self.field[(col, 0)].won != None:
                    self.won = self.field[(col, 0)].won
                    return self.won

        for row in range(3):
            if self.field[(0, row)].won == self.field[(1, row)].won == self.field[(2, row)].won:
                if self.field[(0, row)].won != None:
                    self.won = self.field[(0, row)].won
                    return self.won

        if self.field[(0, 0)].won == self.field[(1, 1)].won == self.field[(2, 2)].won:
            if self.field[(0, 0)].won != None:
                self.won = self.field[(0, 0)].won
                return self.won

        if self.field[(2, 0)].won == self.field[(1, 1)].won == self.field[(0, 2)].won:
            if self.field[(2, 0)].won != None:
                self.won = self.field[(0, 2)].won
                return self.won

        return None

class Game():
    def __init__(self, color: bool) -> None:
        self.color = color

        self.game_field = Field()
        self.current_b_cube = (1, 1)

        self.turn = True

    def render(self) -> None:
        py.draw_rectangle(0, 0, 603, 603, py.Color(222, 222, 222, 255))

        for x in range(3):
            for y in range(3):
                py.draw_rectangle_lines_ex(py.Rectangle(x * 201, y * 201, 201, 201), 3, py.BLACK)
                for x2 in range(3):
                    for y2 in range(3):
                        x_ges = x * 201 + x2 * 67
                        y_ges = y * 201 + y2 * 67
                        py.draw_rectangle_lines(x_ges, y_ges, 67, 67, py.BLACK)

        self.game_field.render()

        if self.game_field.field[self.current_b_cube].won == None:
            if self.turn == self.color:
                py.draw_rectangle_rounded_lines(py.Rectangle(self.current_b_cube[0]*201, self.current_b_cube[1]*201, 201, 201), 0.1, 20, 9.0, py.RED)

            else:
                py.draw_rectangle_rounded_lines(py.Rectangle(self.current_b_cube[0]*201, self.current_b_cube[1]*201, 201, 201), 0.1, 20, 9.0, py.GRAY)

        else:
            if self.turn == self.color:
                py.draw_rectangle_rounded_lines(py.Rectangle(10, 10, 583, 583), 0.1, 20, 9.0, py.RED)

            else:
                py.draw_rectangle_rounded_lines(py.Rectangle(10, 10, 583, 583), 0.1, 20, 9.0, py.GRAY)

    def update(self, conn, profile: Profile) -> None:
        mouse_pos = py.get_mouse_position()

        if mouse_pos.x < 603:
            t_big_cube = (mouse_pos.x // 201, mouse_pos.y // 201)
            t_small_cube = (mouse_pos.x%201//67, mouse_pos.y%201//67)

            if py.is_mouse_button_pressed(py.MouseButton.MOUSE_BUTTON_LEFT) and self.game_field.won == None:
                self.set_cube(t_big_cube, t_small_cube, self.color, conn)

        if self.game_field.won == self.color:
            profile.game_result(conn.opp_data, True)

        elif self.game_field.won == (not self.color):
            profile.game_result(conn.opp_data, False)

    def set_cube(self, b_pos: tuple, s_pos: tuple, color: bool, conn = None):
        print(self.current_b_cube, b_pos)
        print(self.turn, self.color)
        if color == self.turn and (self.current_b_cube == b_pos or self.game_field.field[self.current_b_cube].won != None) and self.game_field.field[b_pos].field[s_pos].color == None and self.game_field.field[b_pos].won == None:
            self.turn = not self.turn
            self.game_field.set_cube(b_pos, s_pos, color)

            self.current_b_cube = s_pos

            if conn != None:
                conn.send(b_pos, s_pos)
