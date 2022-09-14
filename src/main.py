from tft import Tft
from time import sleep
from rich import print_json
from json import dumps
from os import system


tft = Tft()

prev_state = None
while True:
	state = tft.get_gamestate()
	if state != prev_state:
		system('cls')
		print_json(dumps(state))
	prev_state = state
	sleep(0.1)
