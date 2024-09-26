import pyray as py
import time

def ease_in(t: float) -> float:
    return 4 * t * t * t

def ease_out(t: float) -> float:
    return 4 * (t - 1) * (t - 1) * (t - 1) + 1

def ease_in_out(t: float) -> float:
    if t < 0.5:
        return ease_in(t)
    else:
        return ease_out(t)

class Transition():
    def __init__(self, new: str, dur: float, hold: float) -> None:
        self.new = new

        self.dur = dur

        self.last_time = 0
        self.delta_time = 0

        self.hold_counter = 0
        self.hold = hold

        self.counter = 0
        self.completion = 0
        self.height = 0

        self.first = True
        self.direction = "in"

        self.can_change = False
        self.finshed = False

    def update(self) -> None:
        if self.finshed:
            return
        
        if self.first:
            self.last_time = time.time()
            self.first = False

        self.delta_time = (time.time() - self.last_time) * 1000
        self.last_time = time.time()

        if self.direction == "in":
            self.counter += self.delta_time

            self.completion = self.counter / self.dur
            self.height = 603 * ease_in(self.completion)

            if self.completion >= 1:
                self.direction = "hold"

        if self.direction == "out":
            self.counter -= self.delta_time

            self.completion = (self.counter / self.dur)
            self.height = 603 * ease_out(self.completion)

            if self.counter <= 0:
                self.finshed = True

        if self.direction == "hold":
            self.hold_counter += self.delta_time
            if self.hold_counter >= self.hold:
                self.direction = "out"

            self.can_change = True

    def render(self) -> None:
        py.draw_rectangle(0, 0, 900, int(self.height), py.DARKGREEN)
