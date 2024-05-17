from tkinter import *
import random
from dataclasses import dataclass, field

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"


@dataclass
class Snake:
    body_size: int = BODY_PARTS
    coordinates: list = field(default_factory=lambda: [])
    squares: list = field(default_factory=lambda: [])

    def __post_init__(self):
        for i in range(self.body_size):
            self.coordinates.append([0, 0])

        for snakes_x, snakes_y in self.coordinates:
            square = canvas.create_rectangle(
                snakes_x,
                snakes_y,
                snakes_x + SPACE_SIZE,
                snakes_y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tags="snake",
            )
            self.squares.append(square)


@dataclass
class Food:
    coordinates: list = field(default_factory=lambda: [])

    def __post_init__(self):
        foods_x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        foods_y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [foods_x, foods_y]

        canvas.create_oval(
            foods_x,
            foods_y,
            foods_x + SPACE_SIZE,
            foods_y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tags="food",
        )


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text=f"Score: {score}")

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    collisions_x, collisions_y = snake.coordinates[0]

    if collisions_x < 0 or collisions_x >= GAME_WIDTH:
        return True
    elif collisions_y < 0 or collisions_y >= GAME_HEIGHT:
        print("GAME OVER")
        return True

    for body_part in snake.coordinates[1:]:
        if collisions_x == body_part[0] and collisions_y == body_part[1]:
            print("GAME OVER")
            return True

    return False


def restart_game():
    global score, direction, snake, food, highest_score

    if score > highest_score:
        highest_score = score
        save_highest_score(highest_score)

    highest_score_label.config(text=f"Highest Score: {highest_score}")

    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")
    canvas.delete("snake", "food", "gameover")
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    restart_button.config(state=DISABLED)

    highest_score_label.place(x=10, y=17)


def game_over():
    global highest_score
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text=f"GAME OVER\nHighest Score: {highest_score}",
        fill="red",
        tags="gameover",
    )
    restart_button.config(state=NORMAL)


def load_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


highest_score = load_highest_score()


def save_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


window = Tk()
window.title("Snake game")
window.resizable(False, False)
window.iconbitmap("snake_icon.ico")

score = 0
direction = "down"
label = Label(
    window,
    text=f"Score: {score}",
    font=("consolas", 40),
)
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()

center_window(window, window_width, window_height)

restart_button = Button(
    window, text="Restart", font=("consolas", 20), command=restart_game
)
restart_button.pack()
restart_button.place(relx=0.9, rely=0.045, anchor=CENTER)
restart_button.config(state=DISABLED)

highest_score_label = Label(
    window, text=f"Highest Score: {highest_score}", font=("consolas", 20)
)
highest_score_label.place(x=10, y=17)

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
