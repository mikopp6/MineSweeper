"""
MineSweeper
@author Miko Palojärvi, github.com/mikopp6

Minesweeper game made with python, for University of Oulu Elementary Programming course.

"""

import random
import sys
import time
import json
from datetime import datetime, timedelta
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
    "current_status": "In progress",
    "shown_field": [],
    "hidden_field": [],
    "mines_flagged": 0,
    "elapsed_time": 0,
    "time_to_quit": 9999
}

def mouse_handler(x, y, button, modifiers):
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
        x = settings["window_width"]-80,
        y = settings["window_height"]-40,
        font = "roboto",
        size = 24
    )
    sweeperlib.draw_text(
        text = game_status["current_status"],
        x = settings["window_width"]/2-100,
        y = settings["window_height"]-40,
        font = "roboto",
        size = 24
    )

    
def interval_handler(elapsed):
    if game_status["current_status"] == "In progress":
        game_status["elapsed_time"] += elapsed

    if game_status["elapsed_time"] >= game_status["time_to_quit"]:
        sweeperlib.close()  
    elif game_status["current_status"] != "In progress" and game_status["time_to_quit"] == 9999:
        game_status["time_to_quit"] = game_status["elapsed_time"] + 5
        save_stats()

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
            game_status["shown_field"][row][column] = "x"
            game_status["current_status"] = "You lost!"
        elif square == " ":
            floodfill(column, row)
    elif button == 4:
        if game_status["shown_field"][row][column] == " ":
            game_status["shown_field"][row][column] = "f"
            if square == "x":
                game_status["mines_flagged"] += 1
                if game_status["mines_flagged"] == settings["mines"]:
                    game_status["current_status"] = "You won!"
        elif game_status["shown_field"][row][column] == "f":
            game_status["shown_field"][row][column] = " "
            if square == "x":
                game_status["mines_flagged"] -= 1
        

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
    game_status["current_status"] = "In progress"
    game_status["shown_field"] = []
    game_status["hidden_field"] = []
    game_status["mines_flagged"] = 0
    game_status["elapsed_time"] = 0
    game_status["time_to_quit"] = 9999


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
            show_stats()
        elif menu_choice == "q":
            print("Thanks for playing!")
            break
        else:
            print("Incorrect choice")

def game():
    reset_game_status()

    while True:
        print("\nDifficulty?")
        print("(E)asy - 9x9, 10 mines")
        print("(M)edium - 16x16, 40 mines")
        print("(H)ard - 16x30, 99 mines")
        print("(C)ustom")
        print("(B)ack to menu")
        game_choice = input("Choose: ").strip().lower()
        if game_choice == "e":
            settings["height"] = 9
            settings["width"] = 9
            settings["mines"] = 10
            break
        elif game_choice == "m":
            settings["height"] = 16
            settings["width"] = 16
            settings["mines"] = 40
            break
        elif game_choice == "h":
            settings["height"] = 16
            settings["width"] = 30
            settings["mines"] = 99
            break
        elif game_choice == "c":
            try:
                settings["height"] = int(input("Height: "))
                settings["width"] = int(input("Width: "))
                settings["mines"] = int(input("Mines: "))
            except ValueError:
                print("Please input whole numbers only!")
            else:
                break
        elif game_choice == "b":
            return
        else:
            print("Incorrect choice")
    
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
    sweeperlib.start()

def save_stats():
    game_time = "{:.0f}".format(timedelta(seconds=game_status["elapsed_time"]))
    mine_status = "{}/{}".format(game_status["mines_flagged"], settings["mines"])
    date_and_time = datetime.now().strftime("$D.$M.$Y %H:%M")

    game_statistics = {
        "Date and time: ": date_and_time,
        "Duration: ": game_time,
        "Outcome: ": game_status["current_status"],
        "Mines flagged: ": mine_status
    }

    with open("stats.json", "w") as file:
        json.dump(game_statistics, file, indent=2)


def show_stats():
    try:
        with open("stats.json") as file:
            loaded_stats = json.load(file)
    except (IOError, json.JSONDecodeError):
        print("Unable to find stats.json, try playing first?")
    else:
        print(loaded_stats)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram was interrupted with ctrl-c")