from graphics import *
from obstacles import *
from waiter import *
from shortest_path import *
from math import sqrt
from random import randrange, randint


#Settings - create a button in the main menu


TABLE_RADIUS = 12
TABLE_COLOR = "brown"

CHAIR_SIDE = 6
CHAIR_COLOR = "green"

WAITER_COLOR = "blue"
WAITER_RADIUS = 4
WAITER_ANCHOR = (WAITER_RADIUS * 1.2, WAITER_RADIUS * 1.2)
WAITER_SPEED = 200

DOCKING_RADIUS = WAITER_RADIUS * 1.2

TOLERANCE = 0.5

def generate_random_obstacles(number):
    docking_interception = False
    obstacle_interception = False
    obstacle_types = ["chair", "table", "table"]
    for obstacle in range(number):
        while True:
            obstacle_type = obstacle_types[randint(0, 2)]
            if obstacle_type == "chair":
                obstacle_settings = (randint(CHAIR_SIDE, 100 - CHAIR_SIDE), randint(CHAIR_SIDE, 100 - CHAIR_SIDE))
            elif obstacle_type == "table":
                obstacle_settings = (
                    randint(TABLE_RADIUS, 100 - TABLE_RADIUS), randint(TABLE_RADIUS, 100 - TABLE_RADIUS))
            for obstacle in obstacle_list:
                current_obstacle = obstacle.anchor
                current_center = (current_obstacle.getX(), current_obstacle.getY())
                if obstacle.shape == "square":
                    if obstacle_type == "chair":
                        obstacle_interception = square_square_interception(current_center, CHAIR_SIDE, obstacle_settings, CHAIR_SIDE, 2 * WAITER_RADIUS)
                    else:
                        obstacle_interception = circle_square_interception(
                            current_center, CHAIR_SIDE, obstacle_settings, TABLE_RADIUS, 2 * WAITER_RADIUS)
                else:
                    if obstacle_type == "chair":
                        obstacle_interception = circle_square_interception(
                            obstacle_settings, CHAIR_SIDE, current_center, TABLE_RADIUS, 2 * WAITER_RADIUS)
                    else:
                        obstacle_interception = circle_circle_interception(
                            obstacle_settings, TABLE_RADIUS, current_center, TABLE_RADIUS, 2 * WAITER_RADIUS)
                if obstacle_interception:
                    break
            for station in docking_stations:
                current_station = station.body.getCenter()
                current_center = (current_station.getX(), current_station.getY())
                if obstacle_type == "chair":
                    docking_interception = circle_square_interception(
                        obstacle_settings, CHAIR_SIDE, current_center, station.radius, 2 * WAITER_RADIUS)
                else:
                    docking_interception = circle_circle_interception(
                        obstacle_settings, TABLE_RADIUS, current_center, station.radius, 2 * WAITER_RADIUS)
                    
                if docking_interception:
                    break
          
            if docking_interception or obstacle_interception:
                continue

            else:
                if obstacle_type == "chair":
                    chair = Chair(CHAIR_COLOR, obstacle_settings, CHAIR_SIDE)
                else:
                    table = Table(TABLE_COLOR, obstacle_settings, TABLE_RADIUS)
                break



def main():
    win = GraphWin("Trial version", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("white")
    docking1 = Docking((DOCKING_RADIUS, DOCKING_RADIUS), DOCKING_RADIUS)
    docking1.draw(win)
    docking2 = Docking((100 - DOCKING_RADIUS, 100 - DOCKING_RADIUS), DOCKING_RADIUS)
    docking2.draw(win)
    generate_random_obstacles(8)
    for obstacle in obstacle_list:
        obstacle.draw(win)
    waiter = Waiter1(WAITER_COLOR, WAITER_RADIUS, WAITER_ANCHOR, TOLERANCE,
                    WAITER_SPEED, obstacle_list, win)
    waiter.draw()
    waiter.clean_room(docking_stations)
    waiterb = Waiter23(WAITER_COLOR, WAITER_RADIUS, WAITER_ANCHOR, TOLERANCE,
                     WAITER_SPEED, obstacle_list, win)
    waiterb.draw()
    waiterb.clean_whole_room(docking_stations)#docking_stations)

    win.getMouse()
    win.close()

main()






