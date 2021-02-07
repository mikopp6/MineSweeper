"""
MineSweeper
@author Miko Palojärvi, github.com/mikopp6

Minesweeper game made with python, for University of Oulu Elementary Programming course.

"""

import random
from datetime import datetime
from math import floor
import sweeperlib

"""
settings, mouse_buttons and game_status
Required variables for controlling game logic and state.
Does what their name implies.
"""
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
    "time_to_quit": 0
}

def mouse_handler(x, y, button, modifiers):
    """
    Handler function for mouse.
    If mouse clicked inside playarea, calls check_square with coords.
    More info on how this is used in sweeperlib.py.

    param: x, y: x and y position of click
    param: button: which button is clicked
    param: modifiers: not used
    """

    column = floor(x / 40)
    row = floor(y / 40)
    if column < settings["width"] and row < settings["height"]:
        check_square(row, column, button)

def draw_handler():
    """
    Handler function for drawing.
    Prepares sprites for shown_field, and draws them. 
    Also draws clock and current game status.    
    More info on how this is used in sweeperlib.py.
    """

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
    """
    Handler function for interval. 
    Used for controlling game clock, with added logic for when to close the game.
    More info on how this is used in sweeperlib.py.

    param: elapsed: actual time elapsed
    """

    if game_status["current_status"] == "In progress":
        game_status["elapsed_time"] += elapsed
    elif game_status["time_to_quit"] > 5:
        save_stats()
        sweeperlib.close()  
    elif game_status["current_status"] != "In progress":
        game_status["time_to_quit"] += elapsed

def create_field():
    """
    Creates 2 minefields, hidden and shown.
    Hidden is used to get mine positions, and shown is used to show the field to the player without the mines.
    """

    game_status["hidden_field"] = []
    for _ in range(settings["height"]):
        game_status["hidden_field"].append([])
        for _ in range(settings["width"]):
            game_status["hidden_field"][-1].append(" ")

    game_status["shown_field"] = [row[:] for row in game_status["hidden_field"]]

def insert_mines():
    """
    Inserts mines to the hidden field. Positions are chosen randomly
    """

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
    """
    Checks clicked square. 
    Does different things depending on which mouse button is given, and what the square contains.

    param: row: row position of click
    param: column: column position of click
    param: button: button used in click
    """

    square = game_status["hidden_field"][row][column]
    if button == 1:
        if square == "x":
            game_status["shown_field"] = game_status["hidden_field"]
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
    Using modified floodfill to open up playarea, minesweeper style.
    Adds squares to be checked to checklist, 
    calls count_surroundings to count number of mines,
    and pops them off after check.

    param: starting_x: x position on where to start
    param: starting_y: y position on where to start
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
    """
    Counts how many mines surrounds the given position, and returns the value.

    param: x, y: x and y position to check
    """

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
    """
    Resets all game statuses to defaults
    """

    game_status["current_status"] = "In progress"
    game_status["shown_field"] = []
    game_status["hidden_field"] = []
    game_status["mines_flagged"] = 0
    game_status["elapsed_time"] = 0
    game_status["time_to_quit"] = 0


def menu():
    """
    Main menu for the game.
    """

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
    """
    New game menu. Depending on user input, creates minefield, 
    attaches handlers to helper library and starts game.
    """

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
                if settings["mines"] == 0:
                    print("Not enough mines!")
                elif settings["mines"] > settings["height"]*settings["width"]:
                    print("Too many mines!")
                else:
                    break
        elif game_choice == "b":
            return
        else:
            print("Incorrect choice")
    
    reset_game_status()
    settings["window_width"] = settings["width"]*40
    settings["window_height"] = settings["height"]*40+40

    create_field()
    insert_mines()

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(settings["window_width"], settings["window_height"], settings["background_color"])
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_draw_handler(draw_handler)
    sweeperlib.set_interval_handler(interval_handler)
    sweeperlib.start()

def save_stats():
    """
    Used to save statistics after game. Saves to stats.txt
    """

    date_and_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    m, s = divmod(int(game_status["elapsed_time"]), 60)
    game_time = "{:02d}:{:02d}".format(m, s)
    mine_status = "{}/{}".format(game_status["mines_flagged"], settings["mines"])
    
    game_statistics = {
        "Date and time": date_and_time,
        "Duration": game_time,
        "Outcome": game_status["current_status"],
        "Mines flagged": mine_status
    }

    with open("stats.txt", "a+") as file:
        file.write(str(game_statistics) + "\n")


def show_stats():
    """
    Used to show player the statistics of previously played games.
    """

    try:
        with open("stats.txt") as file:
            loaded_stats = file.read()
    except (IOError):
        print("Unable to find stats.txt, try playing first?")
    else:
        print(loaded_stats)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram was interrupted with ctrl-c")