import turtle
import random
import string
import time

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Hacker Animation")
screen.setup(width=800, height=600)

start_x, start_y = -screen.window_width() // 2 + 10, screen.window_height() // 2 - 20
current_x, current_y = start_x, start_y

text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.speed(0)
text_turtle.color("green")
text_turtle.penup()

font = ("Courier", 12, "normal")

line_height = 20
count = 0

messages = [
    "Access Granted",
    "Connection Established",
    "Loading Data...",
    "Decrypting...",
    "System Breach Detected",
    "Analyzing...",
    "Traceback (most recent call last):",
    "Initializing...",
    "Compiling...",
    "Execution Complete"
]
last = len(messages)

def generate_random_text():
    length = random.randint(5, 25)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def type_text(text, speed):
    global current_x, current_y
    for char in text:
        text_turtle.goto(current_x, current_y)
        text_turtle.write(char, font=font)
        current_x += 8
        screen.update()
        time.sleep(speed)
    current_x = start_x 
    current_y -= line_height

# Input commands
comman = float(input("Enter command threshold: "))
speed = float(input("Enter typing speed (seconds per character): "))

while True:
    if count == last:
        print("lost")
        random_text = "lost"
    elif count < 2:
        random_text = messages[count]
        count += 1
        print(messages[count])
    elif random.random() < comman:
        text_turtle.color("green")
        random_text = messages[count]
        print(messages[count])
        count += 1
    else:
        text_turtle.color("red")
        random_text = generate_random_text()
        print(generate_random_text())
    
    type_text(random_text, speed)

    print("[", current_y, ",", current_x, "]")
    if current_y < -screen.window_height() // 2:
        current_y = start_y
        text_turtle.clear()
        current_x, current_y = start_x, start_y

turtle.done()
