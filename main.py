import pyray as py
import os

from scripts.game import Game
from scripts.menu import Main, NewAcc, ConnectToIn
from scripts.server import Server
from scripts.client import Client
from scripts.profile import Profile
from scripts.transition import Transition
from scripts.load_anim import LoadingAnim

def new_game(profile: Profile) -> tuple[Game, Server]:
	game = Game(True)
	server = Server(game, profile)

	return (game, server)

def connect_to_game(profile: Profile, ip_port: str) -> tuple[Game, Client]:
	game = Game(False)
	client = Client(ip_port, game, profile)

	return (game, client)

def main() -> None:
	py.init_window(900, 603, "TEST")
	py.set_target_fps(24)

	menu_main = Main()
	menu_new_acc = NewAcc()
	menu_connect_in = ConnectToIn()

	current = "menu_main"
	current_transition = None
	game = None
	conn = None

	base_path = os.path.dirname(os.path.abspath(__file__))
	print(base_path)

	load_from_file = False
	if os.path.exists(base_path + "/data/pr.ttt") and os.path.exists(base_path + "/data/log.ttt"):
		load_from_file = True

	else:
		current = "new_acc"

	profile = Profile("", base_path, load_from_file)

	opp_data = ("__NONE", 0)
	ip_port = ""

	loading_anim = LoadingAnim()

	while not py.window_should_close():
		loading_anim.update()

		if current_transition != None:
			current_transition.update()

			if current_transition.can_change:
				current = current_transition.new

			if current_transition.finshed:
				current_transition = None

		elif current == "menu_main":
			game = None
			next = menu_main.update()

			if next != "NONE":
				current_transition = Transition(next, 600, 5)

		elif current == "game":
			conn.update()
			game.update(conn, profile)

			if game.finished:
				conn.close()
				conn = None
				current_transition = Transition("menu_main", 600, 5)

		elif current == "create":
			if game == None:
				game, conn = new_game(profile)

			if conn.check_connecting():
				current_transition = Transition("game", 600, 5)
				profile.game_start()
				opp_data = conn.opp_data

		elif current == "connect":
			next = menu_connect_in.update()
			if next != "NONE":
				current_transition = Transition(next, 600, 5)
				ip_port = menu_connect_in.ip_port

		elif current == "connect_2":
			if game == None:
				game, conn = connect_to_game(profile, ip_port)

			if conn.check_connection():
				current_transition = Transition("game", 600, 5)
				profile.game_start()
				opp_data = conn.opp_data

		elif current == "new_acc":
			next = menu_new_acc.update()
			if next != "NONE":
				current_transition = Transition(next, 600, 5)
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

		elif current == "create":
			if conn != None:
				py.draw_text("Lobbycode: '" + conn.code + "'", 50, 200, 20, py.RAYWHITE)
				py.draw_text("Please enter this code to join", 50, 250, 20, py.RAYWHITE)
			
			loading_anim.render("Waiting for Players")

		elif current == "connect":
			menu_connect_in.render()
			py.draw_text("Please enter a Lobbycode to join", 50, 250, 20, py.RAYWHITE)
			py.draw_text("(cltr + v to paste)", 50, 300, 20, py.RAYWHITE)

		elif current == "connect_2":
			loading_anim.render("Connecting")

		if current_transition != None:
			current_transition.render()

		py.draw_fps(5, 5)
		py.end_drawing()

	py.close_window()

	if conn != None:
		conn.close()

	print("GAME CLOSED")

if __name__ == '__main__':
	main()
