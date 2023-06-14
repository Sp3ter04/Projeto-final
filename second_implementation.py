from graphics import *
from universal_functions import default_restaurant_generator
from waiter import Waiter23
from obstacles import *
from settings import get_settings

# TABLE_RADIUS = 12
# CHAIR_SIDE = 6
# WAITER_RADIUS = 4
# WAITER_SPEED = 200
# DOCKING_RADIUS = WAITER_RADIUS * 1.2
# TOLERANCE = 0.5
# SHOW_GRID = False
# SHOW_CLEANED = True


def second_implementation():
    TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS, WAITER_SPEED, SHOW_GRID, SHOW_CLEANED, DOCKING_RADIUS, TOLERANCE = get_settings()
    win = GraphWin("Segunda Implementação", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color_rgb(61, 36, 1))
    carpet = Rectangle(Point(WAITER_RADIUS, WAITER_RADIUS),
                       Point(100 - WAITER_RADIUS, 100 - WAITER_RADIUS))
    carpet.setFill(color_rgb(217, 202, 165))
    carpet.draw(win)
    docking1 = Docking((DOCKING_RADIUS, DOCKING_RADIUS), DOCKING_RADIUS)
    docking2 = Docking((100 - DOCKING_RADIUS, 100 -
                       DOCKING_RADIUS), DOCKING_RADIUS)
    for station in docking_stations:
        station.draw(win)
    default_restaurant_generator(TABLE_RADIUS, CHAIR_SIDE)
    for obstacle in obstacle_list:
        obstacle.draw(win)
    waiter = Waiter23(WAITER_RADIUS, TOLERANCE, WAITER_SPEED, docking_stations, win, SHOW_GRID, SHOW_CLEANED)
    waiter.clean_whole_room()
    win.close()


if __name__ == "__main__":
    second_implementation()
    exit()
