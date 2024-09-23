import socket
import threading

from scripts.game import Game
from scripts.profile import Profile

class Client():
    def __init__(self, ip_port: str, game: Game, profile: Profile) -> None:
        self.game = game

        self.host_ip, self.port = ip_port.split(":")
        self.port = int(self.port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.thread = threading.Thread(target=self.connect)
        self.thread.start()

        self.profile = profile

        self.opp_data = ("", 0)

        self.do_close = False
        self.can_close = False

    def connect(self) -> None:
        self.socket.connect((self.host_ip, self.port))
        print(self.socket.getpeername())
        self.socket.send(str((self.profile.name, self.profile.level)).encode(encoding="utf-8"))

        self.opp_data = eval(self.socket.recv(1024).decode(encoding="utf-8"))

    def check_connection(self) -> bool:
        if self.thread.is_alive():
            return False
        
        print("Connected")
        return True
    
    def update(self) -> None:
        if not self.thread.is_alive() and not self.do_close:
            self.thread = threading.Thread(target=self._update)
            self.thread.start()
    
    def _update(self) -> None:
        if self.do_close:
            return
                
        print("receving")
        msg = self.socket.recv(1024).decode("utf-8")
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
        msg = f"placed:({b_cube},{s_cube})"

        thread = threading.Thread(target=self._send, args=(msg,))
        thread.start()

    def _send(self, msg: str) -> None:
        print("sending", msg)
        self.socket.send(msg.encode("utf-8"))

    def close(self) -> None:
        self.do_close = True

        msg = "quit"
        thread = threading.Thread(target=self._send, args=(msg,))
        thread.start()

        self.thread.join()

        self.socket.close()
