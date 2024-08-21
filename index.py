import turtle
import random

screen = turtle.Screen()
t = turtle.Turtle()
count = 0

class Move:
    @staticmethod
    def moveF():
        number = random.randint(0, 1000)
        return number
    
    @staticmethod
    def moveA():
        number = random.randint(0, 360)
        return number
    
    @staticmethod
    def check(t):
        screen = t.getscreen()
        screen_width = screen.window_width() // 2
        screen_height = screen.window_height() // 2
        x, y = t.position()
        if abs(x) > screen_width or abs(y) > screen_height:
            print("0x1")
            return True
        print("0x0")
        return False
    
    @staticmethod
    def random_color():
        return (random.random(), random.random(), random.random())
    
    @staticmethod
    def change_colors(t):
        screen = t.getscreen()
        pen_color = Move.random_color()
        background_color = Move.random_color()
        t.pencolor(pen_color)
        screen.bgcolor(background_color)
    
    @staticmethod
    def change(t):
        screen = t.getscreen()
        screen_width = screen.window_width() // 2
        screen_height = screen.window_height() // 2
        random_x = random.randint(-screen_width, screen_width)
        random_y = random.randint(-screen_height, screen_height)
        t.penup()
        t.goto(random_x, random_y)
        t.pendown()
    
    @staticmethod
    def init(t, count):
        t.forward(Move.moveF())
        if Move.check(t):
            num = random.randint(1, 2)
            if num == 1:
                print("1x0")
                t.left(180)
            else:
                print("1x1")
                t.right(180)
            count += 1
            print(f"2x{count}")
        else:
            count = 0
            print(f"2x{count}")
            num = random.randint(1, 2)
            if num == 1:
                print("1x0")
                t.left(Move.moveA())
            else:
                print("1x1")
                t.right(Move.moveA())
        Move.change_colors(t)
        print(t.position())
        if count >= 1:
            #move.change(t)
            
            t.penup()
            t.goto(0, 0)
            t.pendown()
            
            count = 0
            print(f"2x{count}")

            num = random.randint(1, 2)
            if num == 1:
                print("1x0")
                t.left(Move.moveA())
            else:
                print("1x1")
                t.right(Move.moveA())
        return count

while True:
    t.hideturtle()
    count = Move.init(t, count)
