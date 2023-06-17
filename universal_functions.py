
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""
from math import sqrt
from graphics import *
from random import randint
from obstacles import *


def get_distance(p1, p2):
    delta_x = p1.getX() - p2.getX()
    delta_y = p1.getY() - p2.getY()
    distance = sqrt(delta_x**2 + delta_y**2)
    return delta_x, delta_y, distance

def circle_circle_interception(p1, radius1, p2, radius2, tolerance=0):
    if sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1])**2) <= radius1 + radius2 + tolerance:
        return True
    else:
        return False


def circle_square_interception(p1, width, p2, radius, tolerance=0):
    interception_points = []
    for point in [p1, (p1[0] + width, p1[1]), (p1[0], p1[1] + width),
                  (p1[0] + width, p1[1] + width)]:
        if get_distance(Point(point[0], point[1]), Point(p2[0], p2[1]))[2] <= radius + tolerance:
            interception_points.append(point)

    if len(interception_points) != 0:
        return True
    else:
        return False


def square_square_interception(p1, width_1, p2, width_2, tolerance=0):
    interception_points = []
    tolerance = tolerance / 2
    square_1_corners = [p1, (p1[0], p1[1] + width_1),
                        (p1[0] + width_1, p1[1] + width_1), (p1[0] + width_1, p1[1])]
    for point in square_1_corners:
        if p2[0] - tolerance <= point[0] <= p2[0] + width_2 + tolerance \
                and p2[1] - tolerance <= point[1] <= p2[1] + width_2 + tolerance:
            interception_points.append(point)

    if len(interception_points) != 0:
        return True
    else:
        return False
    
def display_error_message(message, win):
    outer_rectangle = Rectangle(Point(30, 88), Point(70, 100))
    outer_rectangle.setFill(color_rgb(184, 162, 125))
    inner_rectangle = Rectangle(Point(32, 90), Point(68, 98))
    inner_rectangle.setFill(color_rgb(217, 202, 165))
    error_message = Text(Point(50, 94), message)
    error_message.setFace("times roman")
    error_message.setStyle("bold")
    error_message.setSize(14)
    error_message.setTextColor(color_rgb(65, 66, 69))
    error_box = [outer_rectangle, inner_rectangle, error_message]
    for entity in error_box:
        entity.draw(win)
    time.sleep(0.8)
    for entity in error_box:
        entity.undraw()


def generate_random_obstacles(number, table_radius, chair_side, waiter_radius, dirty_spots=[]):
    for obstacle in range(number):
        while True:
            obstacle_type, obstacle_settings = obstacle_generator(table_radius, chair_side)
            obstacle_interception = generator_iterator(
                obstacle_list, obstacle_type, obstacle_settings, table_radius, chair_side, 1.4 * waiter_radius)
            docking_interception = generator_iterator(
                docking_stations, obstacle_type, obstacle_settings, table_radius, chair_side, 1.1 * waiter_radius)
            dirt_interception = generator_iterator(
                dirty_spots, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius)
            if docking_interception or obstacle_interception or dirt_interception:
                continue
            if obstacle_type == "chair":
                Chair(obstacle_settings, chair_side)
                break
            else:
                Table(obstacle_settings, table_radius)
                break


def create_station_placeholders(waiter_radius):
    fake_entity_list = []
    docking_1 = Rectangle(Point(0, 0), Point(
            1.2 * waiter_radius, 1.2 * waiter_radius))
    docking_1.anchor = Point(0, 0)
    docking_1.shape = "square"
    docking_1.width = 1.2 * waiter_radius
    fake_entity_list.append(docking_1)
    docking_2 = Rectangle(Point(100 - 1.2 * waiter_radius, 100 - 1.2 * waiter_radius), Point(100, 100))
    docking_2.anchor = Point(
        100 - 1.2 * waiter_radius, 100 - 1.2 * waiter_radius)
    docking_2.shape = "square"
    docking_2.width = 1.2 * waiter_radius
    fake_entity_list.append(docking_2)
    return fake_entity_list

def interception_iterator(entities, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius):
    interceptions = []
    for entity in entities:
        interception = obstacle_interceptions(
            entity, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius)
        if interception:
            interceptions.append(entity)
            break
    if len(interceptions) != 0:
        return True
    return False

def generator_iterator(entity_list, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius):
    fake_entity_list = []
    obstacle_interception = False
    if len(entity_list) == 0:
        fake_entity_list = create_station_placeholders(waiter_radius)
    if len(fake_entity_list) == 0:
        obstacle_interception = interception_iterator(entity_list, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius)
    else:
        obstacle_interception = interception_iterator(
            fake_entity_list, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius)
    return obstacle_interception


def obstacle_generator(table_radius, chair_side):
    obstacle_types = ["chair", "chair", "table", "table", "table", "table"]
    obstacle_type = obstacle_types[randint(0, 5)]
    if obstacle_type == "chair":
        obstacle_settings = (randint(chair_side + 4, 96 - chair_side),
                             randint(chair_side + 4, 96 - chair_side))
    elif obstacle_type == "table":
        obstacle_settings = (
            randint(table_radius + 4, 96 - table_radius), randint(table_radius + 4, 96 - table_radius))
    return obstacle_type, obstacle_settings


def obstacle_interceptions(obstacle, obstacle_type, obstacle_settings, table_radius, chair_side, waiter_radius):
    current_obstacle = obstacle.anchor
    current_center = (current_obstacle.getX(), current_obstacle.getY())
    obstacle_interception = False
    if obstacle.shape == "square":
        if obstacle_type == "chair":
            obstacle_interception = square_square_interception(
                current_center, chair_side, obstacle_settings, chair_side, 2 * waiter_radius)
        else:
            obstacle_interception = circle_square_interception(
                current_center, chair_side, obstacle_settings, table_radius, 2 * waiter_radius)
    else:
        if obstacle_type == "chair":
            obstacle_interception = circle_square_interception(
                obstacle_settings, chair_side, current_center, table_radius, 2 * waiter_radius)
        else:
            obstacle_interception = circle_circle_interception(
                obstacle_settings, table_radius, current_center, table_radius, 2 * waiter_radius)
    return obstacle_interception

def default_restaurant_generator(table_radius, chair_width, waiter_radius):
    tolerance = 2.5 * waiter_radius + chair_width
    get_group((table_radius + tolerance, table_radius +
              tolerance), table_radius, chair_width)
    get_group((100 - table_radius - tolerance, table_radius + tolerance),
              table_radius, chair_width)
    get_group((table_radius + tolerance, 100 - table_radius - tolerance),
              table_radius, chair_width)
    get_group((100 - table_radius - tolerance, 100 - table_radius - tolerance),
              table_radius, chair_width)
    get_group((50, 50), table_radius, chair_width)


def get_group(table, table_radius, chair_width):
    chair1 = (table[0] - chair_width / 2, table[1] - table_radius - chair_width - 0.5)
    chair2 = (table[0] - chair_width / 2, table[1] + table_radius + 0.5)
    chair3 = (table[0] - table_radius - chair_width - 0.5, table[1] - chair_width / 2)
    chair4 = (table[0] + table_radius + 0.5, table[1] - chair_width / 2)
    Table(table, table_radius)
    Chair(chair1, chair_width)
    Chair(chair2, chair_width)
    Chair(chair3, chair_width)
    Chair(chair4, chair_width)

def get_carpet(win):
    carpet = Rectangle(Point(3, 3), Point(97, 97))
    carpet.setFill(color_rgb(217, 202, 165))
    carpet.draw(win)
