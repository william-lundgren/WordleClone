import pygame as pg
import random

'''
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

'''


def draw_text(screen, x, y, w, h, text, color, size=40):
    # draw text
    font = pg.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text, text_rect)


def remove_val(d, val):
    new_dict = d.copy()
    for key in list(d.keys()):
        if d.get(key) == val:
            d.pop(key)
    #return new_dict

class Letter:
    def __init__(self, x, y, width, height, bg_color, letter_col, character=""):
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.width = width
        self.height = height
        self.letter_color = letter_col
        self.char = character.upper()

    def draw(self, display):
        pg.draw.rect(display, self.bg_color, (self.x, self.y, self.width, self.height))
        draw_text(display, self.x, self.y, self.width, self.height, self.char.upper(), self.letter_color)

    def change_color(self, new_col):
        if len(new_col) == 3 and not any(val > 255 for val in new_col):
            self.bg_color = new_col
        else:
            print("Invalid color")


class Game:
    def __init__(self, lines, display, colors):
        # SET CONSTS
        self.word = "TESTA"  # random.choice(lines)
        # lines.remove(self.word)
        self.rows = []  # 2d list
        self.guessed_letters = []
        self.display = display
        self.last_letter = -1
        self.last_row = -1
        self.colors = colors
        self.game_over = False

    def keypress(self, key):
        letter = None
        try:
            letter = chr(key)
        except ValueError:
            print("Invalid key")

        # If key in letters type else special case
        letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Å", "A", "S", "D",
                   "F", "G", "H", "J", "K", "L", "Ö", "Ä", "Z", "X", "C", "V", "B", "N", "M"]

        if letter is not None and letter.upper() in letters and self.can_type():
            # Write letter
            if self.last_letter < 4:
                self.rows[self.last_row + 1][self.last_letter + 1].char = letter.upper()
                self.last_letter += 1

        elif key == pg.K_RETURN:
            if not self.can_type():
                self.make_guess()
                # TODO add win condition here instead and maybe check loss too?
            else:
                self.error("Must be 5 letters")
        elif key == pg.K_BACKSPACE and self.last_letter >= 0 and not self.game_over:
            self.back()

    def draw_board(self):
        for row in self.rows:
            for tile in row:
                tile.draw(self.display)

    def create_keyboard(self):
        pass

    def draw_keyboard(self):
        pass

    def check_win(self):
        return self.join_letters(self.rows[self.last_row]).upper() == self.word.upper()

    def make_guess(self):
        greens = []
        letters_to_check = {}

        for i in range(5):
            letters_to_check[i] = self.word[i]
        # Change colors
        # print(self.last_row)
        # if self.last_row == 4:

        #    print("Loss typ")
        # else:

        # First check all greens since they have priority
        for i, ele in enumerate(self.rows[self.last_row + 1]):
            if self.word[i].upper() == ele.char.upper():
                ele.change_color(self.colors.get("green"))
                #                color_change[ele] = self.colors.get("green")
                letters_to_check.pop(i)
                greens.append(i)

        left = list(letters_to_check.keys())

        for i in left:
            letter = self.rows[self.last_row + 1][i]
            if letter.char in list(letters_to_check.values()):
                print("Found")
                letter.change_color(self.colors.get("yellow"))
                print(list(letters_to_check.values()))
                remove_val(letters_to_check, letter.char.upper())
                print(list(letters_to_check.values()))

            # color_change[ele] = self.colors.get("yellow")

            # print("Removed:", letters_to_check)

        if self.last_row != 4:
            self.last_row += 1
            self.last_letter = -1
        else:
            self.game_over = True

        self.check_win()

    def error(self, message):
        pass

    def back(self):
        # print(self.last_letter)
        if self.last_letter > -1:
            self.rows[self.last_row + 1][self.last_letter].char = ""
            self.last_letter -= 1

    @staticmethod
    def join_letters(letters):
        wrd = ""
        for i in letters:
            wrd += i.char
        return wrd

    def can_type(self):
        return self.last_letter != 4

    def find_guess(self, guess, right):
        pass


def main():
    # SETUP
    pg.init()
    pg.display.set_caption("Wordle")
    WIDTH, HEIGHT = 620, 820
    display = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # COLORS
    white = (255, 255, 255)
    green = (83, 141, 78)
    black = (18, 18, 19)  # Background
    dark_grey = (58, 58, 60)  # Wrong letters and keyboard
    light_grey = (129, 131, 132)  # Unused letters
    yellow = (181, 159, 59)

    colors = {"white": white,
              "green": green,
              "black": black,
              "dark_grey": dark_grey,
              "light_grey": light_grey,
              "yellow": yellow}

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

    # Read words
    with open("words.txt") as f:
        lines = f.readlines()

    game_exit = False

    g = Game(lines, display, colors)

    # Create board
    for i in range(6):  # Rows
        row = []
        for j in range(5):  # Cols
            row.append(Letter(board_left_off + j * (board_letter_size + board_letter_off), board_top_off + i * (board_letter_size + board_letter_off),
                              board_letter_size, board_letter_size, light_grey, white))
        g.rows.append(row)

    # Create keyboard

    while not game_exit:
        display.fill(black)

        g.draw_board()
        g.draw_keyboard()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                g.keypress(event.key)
            # if event.type == pg.MOUSEBUTTONDOWN:
            # print(pg.mouse.get_pos())
            # print(g.last_row)

        # g.check_win()
        pg.display.update()
        clock.tick(60)


'''
    completed = False
    print("P = partly right (right letter wrong place)\nR = right\nW = wrong")
    print("Congratulations, you won!")
    print("(Right word = " + word[:-1] + ")")'''

if __name__ == "__main__":
    main()
