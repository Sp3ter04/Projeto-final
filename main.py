from graphics import *
from obstacles import *
from waiter import *
from math import sqrt

#Settings - create a button in the main menu

# TOLERANCE
# WAITER_SPEED
# TABLE_RADIUS
# CHAIR_SIDE

TABLE_RADIUS = 10
TABLE_COLOR = "brown"

CHAIR_SIDE = 4
CHAIR_COLOR = "green"

WAITER_COLOR = "blue"
WAITER_RADIUS = 2.5
WAITER_ANCHOR = (50, 50)
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
    chair1 = Chair(CHAIR_COLOR, (10, 10), CHAIR_SIDE)
    chair1.draw(win)
    waiter.move(win.getMouse())
    table1 = Table(TABLE_COLOR, (90, 90), TABLE_RADIUS)
    table1.draw(win)
    win.getMouse()
    win.close()

main()






