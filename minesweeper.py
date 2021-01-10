import random
import sweeperlib

settings = {
    "width": 10,
    "height": 10,
    "mines": 10,
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
    "field": [],
    "elapsed_time": 0
}

def mouse_handler(x, y, button, modifiers):
    print("Mouse {} clicked in {}, {}".format(mouse_buttons[int(button)], x, y))

def draw_handler():
    
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for i, row in enumerate(game_status["field"]):
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
    field = []
    for _ in range(settings["height"]):
        field.append([])
        for _ in range(settings["width"]):
            field[-1].append(" ")

    game_status["field"] = field

def insert_mines():
    free_squares = []
    for x in range(settings["width"]):
        for y in range(settings["height"]):
            free_squares.append((x, y))

    for _ in range(settings["mines"]):
        square = random.choice(free_squares)
        free_squares.remove(square)
        x, y = square
        game_status["field"][y][x] = "x"

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
