import socket
import threading

from scripts.game import Game
from scripts.profile import Profile

class Server():
    def __init__(self, game: Game, profile: Profile) -> None:
        self.game = game
        self.profile = profile

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 10000

        while True:
            try:
                self.socket.bind(("localhost", self.port))
                break

            except Exception:
                self.port += 1

        print(self.port)

        self.opp_data = ("", 0)

        self.thread = threading.Thread(target=self.connect)
        self.thread.start()

        self.conn = None
        self.addr = None

        self.can_close = False
        self.do_close = False

    def connect(self) -> None:
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()

        self.opp_data = eval(self.conn.recv(1024).decode(encoding="utf-8"))
        self.conn.send(str((self.profile.name, self.profile.level)).encode(encoding="utf-8"))

    def check_connecting(self) -> bool:
        if self.addr == None:
            return False

        else:
            print("Connected:", self.addr)
            return True
        
    def update(self) -> None:
        if not self.thread.is_alive() and not self.do_close:
            self.thread = threading.Thread(target=self._update)
            self.thread.start()

        if not self.thread.is_alive() and self.do_close:
            self.can_close = True
        
    def _update(self) -> None:
        print("receving")
        msg = self.conn.recv(1024).decode("utf-8")
        print("receved", msg)

        if msg.startswith("placed:"):
            msg = msg[7:]

            b_pos, s_pos = eval(msg)

            self.game.set_cube(b_pos, s_pos, not self.game.color)

        elif msg == "quit":
            msg = "quit"
            self.do_close = True

            thread = threading.Thread(target=self._send, args=(msg,))
            thread.start()

    def send(self, b_cube: tuple, s_cube: tuple) -> None:
        msg = f"placed:({str(b_cube)},{str(s_cube)})"

        thread = threading.Thread(target=self._send, args=(msg,))
        thread.start()

    def _send(self, msg: str) -> None:
        print("sending", msg)
        self.conn.send(msg.encode("utf-8"))

    def close(self) -> None:
        self.do_close = True

        msg = "quit"
        thread = threading.Thread(target=self._send, args=(msg,))
        thread.start()

        self.thread.join()

        #self.conn.close()
