from graphics import *
from obstacles import *
from waiter import *
from shortest_path import *
from math import sqrt
from random import randint


#Settings - create a button in the main menu


TABLE_RADIUS = 12
CHAIR_SIDE = 6
WAITER_RADIUS = 4
WAITER_SPEED = 120

DOCKING_RADIUS = WAITER_RADIUS * 1.2

TOLERANCE = 0.5

def generate_random_obstacles(number):
    obstacle_types = ["chair", "chair", "chair", "table", "table", "table", "table", "table"]
    for obstacle in range(number):
        while True:
            obstacle_type, obstacle_settings = obstacle_generator(obstacle_types)
            obstacle_interception = generator_iterator(obstacle_list, obstacle_type, obstacle_settings)
            docking_interception = generator_iterator(docking_stations, obstacle_type, obstacle_settings)
            if docking_interception or obstacle_interception:
                continue
            if obstacle_type == "chair":
                chair = Chair(obstacle_settings, CHAIR_SIDE)
                break
            else:
                table = Table(obstacle_settings, TABLE_RADIUS)
                break

def generator_iterator(entity_list, obstacle_type, obstacle_settings):
    obstacle_interception = False
    for entity in entity_list:
        obstacle_interception = obstacle_interceptions(entity, obstacle_type, obstacle_settings)
        if obstacle_interception:
            break
    return obstacle_interception

def obstacle_generator(obstacle_types):
    obstacle_type = obstacle_types[randint(0, 7)]
    if obstacle_type == "chair":
        obstacle_settings = (randint(CHAIR_SIDE + 4, 96 - CHAIR_SIDE), randint(CHAIR_SIDE + 4, 96 - CHAIR_SIDE))
    elif obstacle_type == "table":
        obstacle_settings = (
            randint(TABLE_RADIUS + 4, 96 - TABLE_RADIUS), randint(TABLE_RADIUS + 4, 96 - TABLE_RADIUS))
    return obstacle_type, obstacle_settings

def obstacle_interceptions(obstacle, obstacle_type, obstacle_settings):
    current_obstacle = obstacle.anchor
    current_center = (current_obstacle.getX(),current_obstacle.getY())
    obstacle_interception = False
    if obstacle.shape == "square":
        if obstacle_type == "chair":
            obstacle_interception = square_square_interception(
                current_center, CHAIR_SIDE, obstacle_settings, CHAIR_SIDE, 2 * WAITER_RADIUS)
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
    return obstacle_interception



def main():
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
    generate_random_obstacles(8)
    for obstacle in obstacle_list:
        obstacle.draw(win)
    waiter = Waiter1(WAITER_RADIUS, TOLERANCE, WAITER_SPEED, docking_stations, win)
    waiter.clean_room()
    waiter.undraw()
    waiterb = Waiter23(WAITER_RADIUS, TOLERANCE, WAITER_SPEED, docking_stations, win)
    waiterb.clean_whole_room()
    win.close()

main()






