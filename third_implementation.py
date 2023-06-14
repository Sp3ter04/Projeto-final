# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from universal_functions import generate_random_obstacles
from waiter import Waiter23
from obstacles import *
from third_imp_menu import *
from settings import get_settings

def get_menu_options():
    obstacle_menu = third_imp_menu("Obstáculos criados aleatoriamente\n(aleat.ger)", "Obstáculos lidos de um ficheiro\n(sala.txt)",
                                    "random", "file")
    obstacle_mode = obstacle_menu.get_button_press()
    dirt_menu = third_imp_menu("Sujidades introduzidas manualmente", "Sujidades lidas do ficheiro", "manual", "file")
    dirt_mode = dirt_menu.get_button_press()
    return obstacle_mode, dirt_mode

def get_obstacles(obstacles, chair_side, table_radius, docking_radius):
    for obstacle in obstacles:
        if obstacle[0].capitalize() == "Cadeira":
            Chair((float(obstacle[1]), float(obstacle[2])), chair_side)
        elif obstacle[0].capitalize() == "Mesa":
            Table((float(obstacle[1]), float(obstacle[2])), table_radius)
        elif obstacle[0].capitalize() == "Dock":
            Docking((float(obstacle[1]), float(obstacle[2])), docking_radius)
        else:
            print(f"Erro ao carregar o objeto {obstacle[0]}.\nOmitido")


def get_file_obstacles(chair_side, table_radius, docking_radius):
    lines = []
    obstacles = []
    try:
        with open("sala.txt", "r") as file:
            for line in file:
                lines.append(line)
    except Exception as e:
        print(e)
    finally:
        window_size = lines[1].strip().split(" ")
        for line in lines[3:]:
            if len(line.strip()) != 0:
                obstacles.append(tuple(line.strip().split(" ")))
        get_obstacles(obstacles, chair_side, table_radius, docking_radius)
        return window_size

def get_dirt_file(waiter_radius):
    dirty_places = []
    spot = ()
    lines = []
    try:
        with open("dirt.txt", "r") as file:
            for line in file:
                lines.append(line)
            for line in lines[1:]:
                spot = tuple(line.strip().split(" "))
                dirty_places.append(DirtPlaceHolder(Point(spot[0], spot[1]), waiter_radius))
    except Exception as e:
        print(e)
    finally:
        return dirty_places
    
def default_stations(docking_radius):
    Docking((docking_radius, docking_radius), docking_radius)
    Docking((100 - docking_radius, 100 -
                    docking_radius), docking_radius)
    
def menu_interpretation(waiter_radius, chair_side, docking_radius, table_radius):
    obstacle_mode, dirt_mode = get_menu_options()
    if dirt_mode == "quit" or obstacle_mode == "quit":
        return "quit", None
    if obstacle_mode == "file":
        win_size = get_file_obstacles(chair_side, table_radius, docking_radius)
        if dirt_mode == "file":
            dirty_places = get_dirt_file(waiter_radius)
        else:
            dirty_places = []
        return dirty_places, win_size
    if obstacle_mode == "random":
        if dirt_mode == "file":
            dirty_places = get_dirt_file(waiter_radius)
        else:
            dirty_places = []
        generate_random_obstacles(14, table_radius, chair_side, waiter_radius, dirty_places)
        return dirty_places, None

def window_generator(waiter_radius, win_size):
    win = GraphWin("Terceira Implementação", win_size[0], win_size[1])
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color_rgb(61, 36, 1))
    carpet = Rectangle(Point(waiter_radius, waiter_radius),
                    Point(100 - waiter_radius, 100 - waiter_radius))
    carpet.setFill(color_rgb(217, 202, 165))
    carpet.draw(win)
    return win

def third_implementation(win_size=(800, 800), dirty_places=[]):
    while True:
        TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS, WAITER_SPEED, SHOW_GRID, SHOW_CLEANED, DOCKING_RADIUS, TOLERANCE = get_settings()
        dirty_places, temp_win_size = menu_interpretation(WAITER_RADIUS, CHAIR_SIDE,DOCKING_RADIUS, TABLE_RADIUS)
        if dirty_places == "quit":
            break
        if temp_win_size is not None:
            win_size = temp_win_size
        win = window_generator( WAITER_RADIUS,  win_size)
        if len(docking_stations) == 0:
            default_stations(DOCKING_RADIUS)
        for station in docking_stations:
            station.draw(win)
        for obstacle in obstacle_list:
            obstacle.draw(win)
        waiter = Waiter23(WAITER_RADIUS, TOLERANCE,
                          WAITER_SPEED, docking_stations, win, SHOW_GRID, SHOW_CLEANED, dirty_places)
        waiter.clean_whole_room()
        break
    win.close()

if __name__ == "__main__":
    third_implementation()
    exit()
