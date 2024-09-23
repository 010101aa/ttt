import pyray as py
import os

from scripts.game import Game
from scripts.menu import Main, NewAcc
from scripts.server import Server
from scripts.client import Client
from scripts.profile import Profile

def new_game(profile: Profile) -> tuple[Game, Server]:
	game = Game(True)
	server = Server(game, profile)

	return (game, server)

def connect_to_game(profile: Profile) -> tuple[Game, Client]:
	game = Game(False)
	client = Client(int(input("Port: ")), game, profile)

	return (game, client)

def main() -> None:
	py.init_window(900, 603, "TEST")
	py.set_target_fps(24)

	menu_main = Main()
	menu_new_acc = NewAcc()

	current = "menu_main"
	game = None

	base_path = os.path.dirname(os.path.abspath(__file__))
	print(base_path)

	load_from_file = False
	if os.path.exists(base_path + "/data/pr.ttt") and os.path.exists(base_path + "/data/log.ttt"):
		load_from_file = True

	else:
		current = "new_acc"

	profile = Profile("", base_path, load_from_file)

	opp_data = ("__NONE", 0)

	while not py.window_should_close():
		if current == "menu_main":
			next = menu_main.update()
			if next != "NONE":
				current = next

		elif current == "game":

			conn.update()
			game.update(conn, profile)

		elif current == "create":
			if game == None:
				game, conn = new_game(profile)

			if conn.check_connecting():
				current = "game"
				profile.game_start()
				opp_data = conn.opp_data

		elif current == "connect":
			if game == None:
				game, conn = connect_to_game(profile)

			if conn.check_connection():
				current = "game"
				profile.game_start()
				opp_data = conn.opp_data

		elif current == "new_acc":
			next = menu_new_acc.update()
			if next != "NONE":
				current = next
				profile.name = menu_new_acc.name

		py.begin_drawing()
		py.clear_background(py.BLACK)
		
		if current == "menu_main":
			menu_main.render()
			py.draw_text("Hello, " + profile.name, 100, 100, 40, py.ORANGE)

		elif current == "game":
			game.render()
			py.draw_text(opp_data[0], 700, 100, 20, py.RAYWHITE)
			py.draw_text("lv." + str(opp_data[1]), 700, 200, 20, py.RAYWHITE)

		elif current == "new_acc":
			menu_new_acc.render()

		py.draw_fps(5, 5)
		py.end_drawing()

	py.close_window()
	conn.close()
	print("test")

if __name__ == '__main__':
	main()
