import pygame as pg
import random


class Game:
	def __init__(self):
		pass

	def write(self, letter):
		pass


def main():
	with open("words.txt") as f:
		lines = f.readlines()

	word = random.choice(lines)
	lines.remove(word)

	# SETUP
	pg.init()
	pg.display.set_caption("Wordle")
	WIDTH, HEIGHT = 600, 820
	pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	# COLORS
	green = (83, 141, 78)
	black = (18, 18, 19)  # Background
	dark_grey = (58, 58, 60)  # Wrong letters and keyboard
	light_grey = (129, 131, 132)  # Unused letters
	yellow = (181, 159, 59)

	# Keyboard
	outer_row_off = 75
	inner_row_off = 100
	keyboard_letter_top_dist = 8
	keyboard_letter_right_dist = 6
	keyboard_letter_width = 40
	keyboard_letter_height = 60
	big_button_width = 65
	big_button_height = 60

	# Board
	board_left_off = 150
	board_top_off = 95
	board_letter_off = 5
	board_letter_size = 60

	board_keyboard_diff = 125

	game_exit = False

	g = Game()

	while not game_exit:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.KEYDOWN:
				g.write(event.key)

	completed = False
	print("P = partly right (right letter wrong place)\nR = right\nW = wrong")

	while not completed:
		eval = ""
		valid_guess = False
		while not valid_guess:
			guess = input("Enter a guess: ")
			if len(guess) == 5:
				valid_guess = True
			else:
				print("Your guess must be 5 letters long")
		for i, letter in enumerate(guess):
			if letter not in word:
				eval += "W"
			elif word[i] == guess[i]:
				eval += "R"
			else:
				eval += "P"
		print(eval)
		if eval == "RRRRR":
			completed = True

	print("Congratulations, you won!")
	print("(Right word = " + word[:-1] + ")")


if __name__ == "__main__":
	main()
