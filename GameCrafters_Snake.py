#imports
import turtle
import time
import random

#python's turtle square is 20 pixels wide and 20 pixels tall

##screen settings
SCREEN_SIZE = 600

screen = turtle.Screen()
screen.setup(width = SCREEN_SIZE, height = SCREEN_SIZE)
screen.tracer(0)

# Hardcoded boundaries pulled in to avoid macOS window clipping
x_min, x_max = -100, 100
y_min, y_max = -100, 100

# Food only spawns on the 20px grid, fully on screen using pure Python math
def random_food_pos():
    x = random.randrange(x_min, x_max + 1, 20)
    y = random.randrange(y_min, y_max + 1, 20)
    return x, y

#snake
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)

#food
food_head = turtle.Turtle()
food_head.shape("circle")
food_head.color("red")
food_head.penup()
random_x, random_y = random_food_pos()
food_head.goto(random_x, random_y)

#input handling
head.direction = "stop"  
head.last_direction = "stop" # decoupled physical state tracker

#input listener(state updater):
def go_up():
    if head.last_direction != "down":
        head.direction = "up"

def go_down():
    if head.last_direction != "up":
        head.direction = "down"

def go_left():
    if head.last_direction != "right":
        head.direction = "left"

def go_right():
    if head.last_direction != "left":
        head.direction = "right"


#movement function
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
        head.last_direction = "up" 
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
        head.last_direction = "down"
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
        head.last_direction = "left"
    elif head.direction == "right":
        head.setx(head.xcor() + 20)
        head.last_direction = "right"

# 3. Tell the screen to listen for exact keyboard presses
screen.listen()
screen.onkeypress(go_up, "Up")       
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")


#eating and growing logic
segments = []

#reset function (used by both wall and tail collisions)
def reset_game():
    time.sleep(1) # Pause the game briefly
    head.goto(0, 0)
    head.direction = "stop"
    head.last_direction = "stop" # Reset the tracker on death

    # Teleport the dead body segments permanently off-screen
    for segment in segments:
        segment.goto(1000, 1000)

    # Empty the tracking list to start fresh
    segments.clear()


#game loop
delay = 0.1
while True:
    screen.update()

    # 1. Wall Collisions (Tightened to 200 limits for visible Mac window)
    if head.xcor() > 200 or head.xcor() < -200 or head.ycor() > 200 or head.ycor() < -200:
        reset_game()

    # 2. Eating Logic
    if head.distance(food_head) < 20:
        x, y = random_food_pos()
        food_head.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        
        segments.append(new_segment)

    # 3. Move the tail segments in reverse order using .pos() tuple
    for index in range(len(segments) - 1, 0, -1):
        segments[index].goto(segments[index - 1].pos())

    # 4. Move the very first body segment to the head's previous position
    if len(segments) > 0:
        segments[0].goto(head.pos())
           
    # Call the physical movement execution
    move()

    # 5. Tail Collisions (skipping the neck with [1:] and checking < 15 to avoid float errors)
    for segment in segments[1:]:
        if segment.distance(head) < 15:
            reset_game()
            break

    time.sleep(delay)