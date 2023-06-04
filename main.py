from graphics import *
from obstacles import *
from waiter import *
from shortest_path import *
from math import sqrt
from random import randrange


#Settings - create a button in the main menu


TABLE_RADIUS = 12
TABLE_COLOR = "brown"

CHAIR_SIDE = 6
CHAIR_COLOR = "green"

WAITER_COLOR = "blue"
WAITER_RADIUS = 3
WAITER_ANCHOR = (6, 6)
WAITER_SPEED = 200

TOLERANCE = 0.5



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
    waiter.clean_room(obstacle_list, win)
    win.getMouse()
    win.close()

main()






