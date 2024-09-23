import base64
import datetime
import os

class Profile():
    def __init__(self, name: str, base_path: str, from_file: bool) -> None:
        self.name = name
        self.level = 0

        self.base_path = base_path

        self.won = 0
        self.lost = 0
        self.played = 0

        self.log = []

        if from_file:
            self.load()

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
        time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.log.append({"date" : time, "name" : other[0], "level" : other[1], "won" : won})

        if won:
            self.won += 1

        else:
            self.lost += 1

        if won:
            diff = other[1] - self.level
            diff = max(diff, 3)

            perc = diff / other[1]
            to_add = perc * other[1]

            print(to_add, self.level)
            self.level += to_add

    def game_start(self) -> None:
        self.played += 1

    def get_info(self) -> tuple[str, float, tuple[int, int, int]]:
        # returns [name, level, [games won, games, lost, games played]]
        return (self.name, self.level, (self.won, self.lost, self.played))
    
    def delete_fiels(self) -> None:
        os.remove(self.base_path + "/data/pr.ttt")
        os.remove(self.base_path + "/data/log.ttt")

def test():
    pr = Profile("Simon", "/Users/simon/Desktop/programming/PY/big_tic_tac_toe", False)
    pr.game_start()
    pr.game_result(("Yann", 10.75), True)
    pr.save()

    print(pr.load())
