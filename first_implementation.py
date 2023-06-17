# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from universal_functions import default_restaurant_generator, get_carpet
from waiter import Waiter1
from obstacles import *
from settings import get_settings

def first_implementation():
    """Corre a primeira implementação.

    Importa as preferências do utilizador. De seguida, Cria a janela da 
    implementação e gera o restaurante default, com uma carpete, mesas, cadeiras
    e duas docking_stations. Finalmente, cria o robot e corre-o no modo de primeira
    implementação. Quando o utilizador dá a ordem de regressar ao menu, fecha a 
    janela da primeira implementação e termina o programa.(corrido como 
    subprocess a partir do main.py)
    """

    TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS, WAITER_SPEED, SHOW_GRID, \
    SHOW_CLEANED, DOCKING_RADIUS, TOLERANCE = get_settings()
    win = GraphWin("Primeira Implementação", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color_rgb(61, 36, 1))
    get_carpet(win)
    docking1 = Docking((DOCKING_RADIUS, DOCKING_RADIUS), DOCKING_RADIUS)
    docking2 = Docking((100 - DOCKING_RADIUS, 100 - DOCKING_RADIUS), DOCKING_RADIUS)
    for station in docking_stations:
        station.draw(win)
    default_restaurant_generator(TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS)
    for obstacle in obstacle_list:
        obstacle.draw(win)
    waiter = Waiter1(WAITER_RADIUS, TOLERANCE, WAITER_SPEED, docking_stations, win, SHOW_GRID)
    waiter.clean_room()
    win.close()

if __name__ == "__main__":
    """Para evitar que o código seja corrido automaticamente caso este módulo seja
    importado, define-se que este só será corrido caso o módulo seja corrido 
    diretamente.
    """

    first_implementation()
    exit()