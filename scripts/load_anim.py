import pyray as py
import time

class LoadingAnim():
    def __init__(self) -> None:
        self.sector = 0
        self.sector_size = 45

        self.last_time = 0
        self.delta_time = 0

        self.first = True

        self.poin_counter = 0

        self.points = 0
        self.point_delay = 500

    def update(self) -> None:
        if self.first:
            self.last_time = time.time()
            self.first = False

        self.delta_time = (time.time() - self.last_time)
        self.last_time = time.time()

        self.sector += self.delta_time * 100 * 2
        self.poin_counter += self.delta_time * 1000

        if self.poin_counter >= self.point_delay:
            self.poin_counter = 0
            self.points += 1

        if self.points > 3:
            self.points = 0

        print(self.delta_time, self.sector, self.points)

    def render(self, text: str = "NONE") -> None:
        py.draw_circle_gradient(75, 400, 25, py.BLACK, py.RAYWHITE)

        for off in range(0, 360, self.sector_size * 2):
            py.draw_circle_sector(py.Vector2(75, 400), 30, self.sector + off, self.sector + off + self.sector_size, 20, py.BLACK)

        if text != "NONE":
            height = py.measure_text_ex(py.get_font_default(), text + self.points * ".", 10, 0).y
            py.draw_text(text + self.points * ".", 125, int(400 - height / 2), 10, py.RAYWHITE)
