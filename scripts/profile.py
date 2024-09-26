import base64
import datetime
import os
import time

import numpy as np
from scipy.interpolate import make_interp_spline

class Profile():
    def __init__(self, name: str, base_path: str, from_file: bool) -> None:
        self.name = name
        self.level = 0

        self.base_path = base_path

        self.won = 0
        self.lost = 0
        self.played = 0

        self.log = []
        self.current_game_start = 0
        self.current_game_end = 0
        self.time = ""

        if from_file:
            self.load()

        # curve for xp calculation
        x_points = [-100, -75, -50, -25, 0, 25, 50]
        y_points = [0, 15, 25, 60, 100, 130, 150]

        self.spl = make_interp_spline(x_points, y_points, k=3)

    def calculate_xp(self, diff):
        if diff > 50:
            return 170
        
        if diff < -85:
            return 11.5
        
        return self.spl(diff)

    def save(self) -> None:
        save_str = str(
            {
                "name" : self.name,
                "level" : self.level,
                "stats" : {
                    "won" : self.won,
                    "lost" : self.lost,
                    "played" : self.played
                }
            }
        )

        save_bytes = base64.encodebytes(save_str.encode(encoding="utf-8"))
        with open(self.base_path + "/data/pr.ttt", "wb") as file:
            file.write(save_bytes)

        with open(self.base_path + "/data/log.ttt", "wb") as file:
            file.write(base64.encodebytes(str(self.log).encode(encoding="utf-8")))

    def load(self) -> str:
        with open(self.base_path + "/data/pr.ttt", "rb") as file:
            read_bytes = file.read()

        read_str = base64.decodebytes(read_bytes).decode(encoding="utf-8")
        read_dict = eval(read_str)

        self.name = read_dict["name"]
        self.level = read_dict["level"]

        self.won = read_dict["stats"]["won"]
        self.lost = read_dict["stats"]["lost"]
        self.played = read_dict["stats"]["played"]

        with open(self.base_path + "/data/log.ttt", "rb") as file:
            self.log = eval(base64.decodebytes(file.read()).decode(encoding="utf-8"))

        return (str(read_dict), self.log)

    def game_result(self, other: tuple[str, float], won: bool) -> None:
        self.current_game_end = time.time()

        if won:
            self.won += 1

        else:
            self.lost += 1
            to_add = 0

        if won:
            diff = other[1] - self.level
            to_add = round((self.calculate_xp(diff) / 100) * max(1, diff / 4), 2)
            self.level += float(to_add)
            self.level = round(self.level, 2)

            print(to_add)

        self.log.append({"date" : self.time, "length" : round(self.current_game_end - self.current_game_start, 2), "name" : other[0], "level" : other[1], "won" : won, "gained" : float(to_add)})

    def game_start(self) -> None:
        self.played += 1
        self.current_game_start = time.time()
        self.time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    def get_info(self) -> tuple[str, float, tuple[int, int, int]]:
        # returns [name, level, [games won, games lost, games played]]
        return (self.name, self.level, (self.won, self.lost, self.played))
    
    def delete_files(self) -> None:
        os.remove(self.base_path + "/data/pr.ttt")
        os.remove(self.base_path + "/data/log.ttt")

def test():
    pr = Profile("Simon", "/Users/simon/Desktop/programming/PY/big_tic_tac_toe", True)
    #  pr.delete_files()
    pr.game_start()
    for i in range(1):
        pr.game_result(("Yann", 0), True)

    pr.save()

    print(pr.load())
