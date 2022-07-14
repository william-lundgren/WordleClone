import random

with open("words.txt") as f:
	lines = f.readlines()
line = 2 * random.randrange(0, 203)

word = lines[line]

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
print("(Right word = " + word[:-1] +")")
