"""
MineSweeper
@author Miko Palojärvi, github.com/mikopp6

Minesweeper game made with python, for University of Oulu Elementary Programming course.

"""

import random
import sys
import time
from math import floor
import sweeperlib

# --settings and game_status--
# Required variables for controlling game logic and state
# Does what their name implies
# Settings contain user defined settings
settings = {
    "width": 0,
    "height": 0,
    "mines": 0,
    "background_color": (255, 255, 255, 255),
    "window_width": 0,
    "window_height": 0
}

mouse_buttons = {
    1: "left",
    2: "middle",
    4: "right"
}

game_status = {
    "current_status": "",
    "shown_field": [],
    "hidden_field": [],
    "mines_flagged": 0,
    "elapsed_time": 0
}

def mouse_handler(x, y, button, modifiers):
    print("Mouse {} clicked in {}, {}".format(button, x, y))
    column = floor(x / 40)
    row = floor(y / 40)
    if column < settings["width"] and row < settings["height"]:
        check_square(row, column, button)

def draw_handler():
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for i, row in enumerate(game_status["shown_field"]):
        for j, square in enumerate(row):
            sweeperlib.prepare_sprite(square, j*40, i*40)

    sweeperlib.draw_sprites()
    sweeperlib.draw_text(
        text = "{:.0f}".format(game_status["elapsed_time"]),
        x = settings["window_width"]-60,
        y = settings["window_height"]-40,
        font = "roboto",
        size = 24
    )       

def interval_handler(elapsed):
    game_status["elapsed_time"] += elapsed
    
    if game_status["current_status"] == "good":
        print("YOU WON")
        game_status["shown_field"] == game_status["hidden_field"]
        time.sleep(5)
        sweeperlib.close()
    if game_status["current_status"] == "bad":
        print("YOU LOST")
        game_status["shown_field"] == game_status["hidden_field"]
        time.sleep(5)
        sweeperlib.close()

def create_field():
    game_status["hidden_field"] = []
    for _ in range(settings["height"]):
        game_status["hidden_field"].append([])
        for _ in range(settings["width"]):
            game_status["hidden_field"][-1].append(" ")

    game_status["shown_field"] = [row[:] for row in game_status["hidden_field"]]    # This, or deepcopy, or just call create_field again?

def insert_mines():
    free_squares = []
    for x in range(settings["width"]):
        for y in range(settings["height"]):
            free_squares.append((x, y))

    for _ in range(settings["mines"]):
        square = random.choice(free_squares)
        free_squares.remove(square)
        x, y = square
        game_status["hidden_field"][y][x] = "x"
        
def check_square(row, column, button):
    square = game_status["hidden_field"][row][column]
    if button == 1:
        if square == "x":
            game_status["current_status"] = "bad"
        elif square == " ":
            floodfill(column, row)
    elif button == 4:
        game_status["shown_field"][row][column] = "f"
        if square == "x":
            game_status["mines_flagged"] += 1
            if game_status["mines_flagged"] == settings["mines"]:
                game_status["current_status"] = "good"


def floodfill(starting_x, starting_y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """

    checklist = [(starting_x, starting_y)]

    while checklist:
        x, y = checklist.pop()
        surrounds = count_surroundings(x, y)
        game_status["shown_field"][y][x] = surrounds
        game_status["hidden_field"][y][x] = surrounds

        if surrounds == 0:
            for i in range(y-1, y+2):
                if i < 0 or i == settings["height"]:
                    continue
                for j in range(x-1, x+2):
                    if j < 0 or j == settings["width"]:
                        continue
                    elif game_status["hidden_field"][i][j] == " ":
                        checklist.append((j, i))

def count_surroundings(x, y):
    mines = 0
    for i in range(y-1, y+2):
        if i < 0 or i == settings["height"]:
            continue
        for j in range(x-1, x+2):
            if j < 0 or j == settings["width"]:
                continue
            elif game_status["hidden_field"][i][j] == "x":
                mines += 1

    return mines

def reset_game_status():
    game_status["current_status"] = ""
    game_status["shown_field"] = []
    game_status["hidden_field"] = []
    game_status["mines_flagged"] = 0
    game_status["elapsed_time"] = 0


def menu():
    while True:
        print("\n----------------MineSweeper----------------")
        print("(N)ew game")
        print("(S)tats")
        print("(Q)uit")
        menu_choice = input("Choose: ").strip().lower()
        if menu_choice == "n":
            game()
        elif menu_choice == "s":
            stats()
        elif menu_choice == "q":
            print("Thanks for playing!")
            break
        else:
            print("Incorrect choice")

def game():
    while True:
        print("\nDifficulty?")
        print("(E)asy - 9x9, 10 mines")
        print("(M)edium - 16x16, 40 mines")
        print("(H)ard - 16x30, 99 mines")
        print("(C)ustom")
        print("(B)ack to menu")
        game_choice = input("Choose: ").strip().lower()
        if game_choice == "e":
            settings["width"] = 9
            settings["height"] = 9
            settings["mines"] = 10
            break
        elif game_choice == "m":
            settings["width"] = 16
            settings["height"] = 16
            settings["mines"] = 40
            break
        elif game_choice == "h":
            settings["width"] = 16
            settings["height"] = 30
            settings["mines"] = 99
            break
        elif game_choice == "c":
            settings["width"] = 5
            settings["height"] = 5
            settings["mines"] = 25
            break
        elif game_choice == "b":
            return
        else:
            print("Incorrect choice")
    
    print("1",game_status)
    reset_game_status()
    print("2",game_status)

    settings["window_width"] = settings["width"]*40
    settings["window_height"] = settings["height"]*40+40
    create_field()
    insert_mines()

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(
        settings["window_width"], settings["window_height"], settings["background_color"]
    )
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_draw_handler(draw_handler)
    sweeperlib.set_interval_handler(interval_handler)
    print("3",game_status)

    sweeperlib.start()

def stats():
    pass

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram was interrupted with ctrl-c")
