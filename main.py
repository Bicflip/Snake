from tkinter import *
import random


GAME_W = 1000
GAME_H = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 2
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snek")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_W/SPACE_SIZE) - 1)*SPACE_SIZE
        y = random.randint(0, int(GAME_H/SPACE_SIZE) - 1)*SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


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

    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global speed
        if speed >= 50:
            speed -= 20
        score += 1
        label.config(text="Score:{}".format(score))
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


def change_direction(new_dir):
    global direction

    if new_dir == 'left' and direction != 'right':
        if new_dir != 'right':
            direction = new_dir
    elif new_dir == 'right' and direction != 'left':
        if new_dir != 'left':
            direction = new_dir
    elif new_dir == 'up' and direction != 'down':
        if new_dir != 'down':
            direction = new_dir
    elif new_dir == 'down' and direction != 'up':
        if new_dir != 'up':
            direction = new_dir


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_W:
        return True
    elif y < 0 or y >= GAME_H:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('conslas', 70), text="GAME OVER",
                       fill="red", tag="gameover")


window = Tk()
window.title("Snek Game")

score = 0
speed = SPEED
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('italic', 30))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_H, width=GAME_W)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_height()

x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind("w", lambda event: change_direction('up'))
window.bind("a", lambda event: change_direction('left'))
window.bind("s", lambda event: change_direction('down'))
window.bind("d", lambda event: change_direction('right'))
window.bind("r", lambda event: next_turn(snake, food))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
