from graphics import *
from universal_functions import *
from waiter import Waiter23
from obstacles import *

TABLE_RADIUS = 12
CHAIR_SIDE = 6
WAITER_RADIUS = 4
WAITER_SPEED = 120
DOCKING_RADIUS = WAITER_RADIUS * 1.2
TOLERANCE = 0.5

def second_implementation():
    win = GraphWin("Trial version", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color_rgb(61, 36, 1))
    carpet = Rectangle(Point(WAITER_RADIUS, WAITER_RADIUS), Point(100 - WAITER_RADIUS, 100 - WAITER_RADIUS))
    carpet.setFill(color_rgb(217, 202, 165))
    carpet.draw(win)
    docking1 = Docking((DOCKING_RADIUS, DOCKING_RADIUS), DOCKING_RADIUS)
    docking2 = Docking((100 - DOCKING_RADIUS, 100 - DOCKING_RADIUS), DOCKING_RADIUS)
    for station in docking_stations:
        station.draw(win)
    generate_random_obstacles(8, TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS)
    for obstacle in obstacle_list:
        obstacle.draw(win)
    waiter = Waiter23(WAITER_RADIUS, TOLERANCE, WAITER_SPEED, docking_stations, win)
    waiter.clean_whole_room()
    win.close()


if __name__ == "__main__":
    second_implementation()
    exit()