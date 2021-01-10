import random
from math import floor
import sweeperlib

settings = {
    "width": 16,
    "height": 16,
    "mines": 80,
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
    "elapsed_time": 0
}

def mouse_handler(x, y, button, modifiers):
    print("Mouse {} clicked in {}, {}".format(button, x, y))
    column = floor(x / 40)
    row = floor(y / 40)

    if button == 1:
        check_square(row, column)
    if button == 4:
        game_status["shown_field"][row][column] = "f"
        

        


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
        
def check_square(row, column):
    square = game_status["hidden_field"][row][column]
    if square == "x":
        game_status["shown_field"][row][column] = "x"
    if square == " ":
        floodfill(column, row)
    

def floodfill(starting_x, starting_y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """

    checklist = [(starting_x, starting_y)]
    i = 0
    while checklist:
        x, y = checklist.pop()
        game_status["shown_field"][y][x] = "0"
        game_status["hidden_field"][y][x] = "0"

        for i in range(y-1, y+2):
            if i < 0 or i == settings["height"]:
                continue
            for j in range(x-1, x+2):
                if j < 0 or j == settings["width"]:
                    continue
                elif game_status["hidden_field"][i][j] == " ":
                    checklist.append((j, i))
        i += 1

def main():
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(
        settings["window_width"], settings["window_height"], settings["background_color"]
    )
    sweeperlib.set_mouse_handler(mouse_handler)
    sweeperlib.set_draw_handler(draw_handler)
    sweeperlib.set_interval_handler(interval_handler)
    sweeperlib.start()

if __name__ == "__main__":
    settings["window_width"] = settings["width"]*40
    settings["window_height"] = settings["height"]*40+40
    create_field()
    insert_mines()

    main()
