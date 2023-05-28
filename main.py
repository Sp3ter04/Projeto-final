from graphics import *
from obstacles import *
from waiter import *
from gridmaker import *
from math import sqrt
from random import randrange


#Settings - create a button in the main menu

# TOLERANCE
# WAITER_SPEED
# TABLE_RADIUS
# CHAIR_SIDE

TABLE_RADIUS = 12
TABLE_COLOR = "brown"

CHAIR_SIDE = 6
CHAIR_COLOR = "green"

WAITER_COLOR = "blue"
WAITER_RADIUS = 4
WAITER_ANCHOR = (6, 6)
WAITER_SPEED = 100

TOLERANCE = 0.5


def get_distance(p1, p2):
    delta_x = p1.getX() - p2.getX()
    delta_y = p1.getY() - p2.getY()
    distance = sqrt(delta_x**2 + delta_y**2)
    return delta_x, delta_y, distance



def main():
    win = GraphWin("Trial version", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("white")
    waiter = Waiter1(WAITER_COLOR, WAITER_RADIUS, WAITER_ANCHOR, TOLERANCE,\
                      WAITER_SPEED)
    waiter.draw(win)
    chair1 = Chair(CHAIR_COLOR, (randrange(0, 100),
                   randrange(0, 100)), CHAIR_SIDE)
    chair1.draw(win)
    chair2 = Chair(CHAIR_COLOR, (randrange(0, 100),
                   randrange(0, 100)), CHAIR_SIDE)
    chair2.draw(win)
    chair3 = Chair(CHAIR_COLOR, (randrange(0, 100),
                   randrange(0, 100)), CHAIR_SIDE)
    chair3.draw(win)
    table1 = Table(TABLE_COLOR, (randrange(0, 100),
                   randrange(0, 100)), TABLE_RADIUS)
    table1.draw(win)
    table2 = Table(TABLE_COLOR, (randrange(0, 100),
                   randrange(0, 100)), TABLE_RADIUS)
    table2.draw(win)
    table3 = Table(TABLE_COLOR, (randrange(0, 100),
                   randrange(0, 100)), TABLE_RADIUS)
    table3.draw(win)
    while True:
        mouse_click = win.getMouse()
        try:
            path_to_dirt = run_algorithm(100, WAITER_RADIUS, obstacle_list, (waiter.body.getCenter().getX(), waiter.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()), win)
            for point in path_to_dirt:
                waiter.move(Point(point.x_coord + WAITER_RADIUS / 4, point.y_coord + WAITER_RADIUS / 4))
            waiter.move(mouse_click)
        except:
            error_message = Text(Point(50, 94), "Invalid Input")
            error_message.draw(win)
            time.sleep(0.8)
            error_message.undraw()
    win.getMouse()
    win.close()

main()






