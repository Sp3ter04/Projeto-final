# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from universal_functions import generate_random_obstacles, get_carpet
from waiter import Waiter23
from obstacles import *
from third_imp_menu import *
from settings import get_settings

def get_menu_options():
    """Cria os menus.
    
    Cria dois menus e recolhe as preferências do utilizador em relação à 
    localização dos obstáculos e pontos de maior sujidade.
    """
    
    obstacle_menu = third_imp_menu("Obstáculos criados aleatoriamente\n(aleat.ger)", 
                                   "Obstáculos lidos de um ficheiro\n(sala.txt)", "random", "file")
    obstacle_mode = obstacle_menu.get_button_press()
    dirt_menu = third_imp_menu("Sujidades introduzidas manualmente", 
                               "Sujidades lidas do ficheiro", "manual", "file")
    dirt_mode = dirt_menu.get_button_press()
    return obstacle_mode, dirt_mode

def get_obstacles(obstacles, chair_side, table_radius, docking_radius):
    """Cria os obstáculos recolhidos do ficheiro.
    
    Itera a lista de conjuntos tipo-ponto_âncora e, com base no tipo do obstáculo,
    gera o obstáculo correspondente.
    """
    
    for obstacle in obstacles:
        if obstacle[0].capitalize() == "Cadeira":
            Chair((float(obstacle[1]), float(obstacle[2])), chair_side)
        elif obstacle[0].capitalize() == "Mesa":
            Table((float(obstacle[1]), float(obstacle[2])), table_radius)
        elif obstacle[0].capitalize() == "Dock":
            Docking((float(obstacle[1]), float(obstacle[2])), docking_radius)
        else:
            print(f"Erro ao carregar o objeto {obstacle[0]}.\nOmitido") #Caso haja um obstáculo com um tipo inexistente, este é omitido e o utilizador alertado


def get_file_obstacles(chair_side, table_radius, docking_radius):
    """Recolhe do ficheiro os obstáculos a criar.
    
    Abre o ficheiro em modo de leitura e recolhe as dimensões da janela, bem como
    as coordenadas e tipo de todos os obstáculos a criar. Para cada obstáculo, é
    criado um elemento da lista 'obstacles', consistindo este num tuple com três
    valores: tipo de obstáculo, coordenada x da âncora e coordenada y da âncora.
    Devolve as dimensões da janela.
    """
    
    lines = []
    obstacles = []
    try: #Abre o ficheiro em modo de leitura e recolhe o seu conteúdo (armazenado na lista 'lines')
        with open("sala.txt", "r") as file:
            for line in file:
                lines.append(line)
    except Exception as e: #Caso haja um erro na abertura do ficheiro, explicita o erro que ocorreu
        print(e)
    finally: #Não havendo problemas a abrir o ficheiro, interpreta a informação contida neste
        window_size = lines[1].strip().split(" ") #recolhe as dimensões da janela, separando-as pelo espaço
        for line in lines[3:]:
            if len(line.strip()) != 0:
                obstacles.append(tuple(line.strip().split(" "))) #recolhe as informações dos obstáculos (separando-as pelos espaços entre elas)
        get_obstacles(obstacles, chair_side, table_radius, docking_radius) #Cria os obstáculos com as informações recolhidas
        return window_size

def get_dirt_file(waiter_radius):
    """Recolhea localização dos pontos de maior sujidade a partir do ficheiro.
    
    Abre o ficheiro em modo de leitura e interpreta a informação nele contida 
    para extrair a localização dos pontos de maior sujidade.
    Uma vez que a classe Dirt pressupõe uma criação prévia do robot, não é possível
    criar as sujidades imediatamente. Por essa razão, para evitar conflitos entre
    pontos sujos e obstáculos, criam-se placeholders para os pontos sujos, para
    que estes possam ser utilizados como locais a evitar na rotina de criação 
    aleatória de obstáculos.
    """
    
    dirty_places = [] #lista dos placeholders da sujidade
    spot = ()
    lines = []
    try:
        with open("dirt.txt", "r") as file: #Abre o ficheiro em modo de leitura e extrai dele a localização dos pontos sujos
            for line in file:
                lines.append(line)
            for line in lines[1:]:
                spot = tuple(line.strip().split(" ")) #cria o tuple com as coordenadas do ponto sujo
                dirty_places.append(DirtPlaceHolder(Point(spot[0], spot[1]), waiter_radius)) #adiciona o placeholder à lista
    except Exception as e: #Caso haja um erro na abertura do ficheiro, explicita qual o erro que ocorreu
        print(e)
    finally: #Não tendo ocorrido erro nenhum, devolve a lista de placeholders da sujidade
        return dirty_places
    
def default_stations(docking_radius):
    """Cria as docking stations por defeito.
    
    Caso não tenha sido especificada nenhuma localização para as docking stations,
    gera duas estações, uma no canto inferior esquerdo e outra no superior direito.
    """
    
    Docking((docking_radius, docking_radius), docking_radius)
    Docking((100 - docking_radius, 100 -
                    docking_radius), docking_radius)
    
def menu_interpretation(waiter_radius, chair_side, docking_radius, table_radius):
    """Regula a criação da sala com base nas preferências do utilizador.
    
    Recolhe o modo de obtenção dos obstáculos e pontos de maior sujidade. Com base
    nos valores obtidos para cada uma das situações, coordena as funções 
    responsáveis pela criação dessas entidades.
    """
    
    obstacle_mode, dirt_mode = get_menu_options()
    if dirt_mode == "quit" or obstacle_mode == "quit": #Caso o utilizador dê ordem de sair, devolve "quit"
        return "quit", None
    if obstacle_mode == "file":
        win_size = get_file_obstacles(chair_side, table_radius, docking_radius)
        if dirt_mode == "file": #Caso ambas sejam obtidas do ficheiro, lê ambos os ficheiros e cria os objetos
            dirty_places = get_dirt_file(waiter_radius)
        else: #Caso apenas os obstaculos devam ser obtidos a partir do ficheiro, devolve uma lista vazia de placeholders dos pontos sujos
            dirty_places = []
        return dirty_places, win_size
    if obstacle_mode == "random":
        if dirt_mode == "file":
            dirty_places = get_dirt_file(waiter_radius) #Se os obstáculos forem gerados aleatoriamente e as sujidades lidas do ficheiro, recolhe a lista de placeholders da sujidade para limitar a geração de obstáculos
        else:
            dirty_places = [] #Se os obstáculos forem gerados aleatoriamente e as sujidades recolhidas a partir de clicks, gera obstáculos sem limitação dos placeholders
        generate_random_obstacles(14, table_radius, chair_side, waiter_radius, dirty_places)
        return dirty_places, None

def window_generator(waiter_radius, win_size):
    """Cria a janela da terceira implementação e decora-a com uma carpete."""
    win = GraphWin("Terceira Implementação", win_size[0], win_size[1])
    win.setCoords(0, 0, 100, 100)
    win.setBackground(color_rgb(61, 36, 1))
    get_carpet(win)
    return win

def third_implementation(win_size=(800, 800), dirty_places=[]):
    """Corre a terceira implementação.

    Importa as preferências do utilizador. Em seguida, cria uma lista de pontos 
    sujos e outra de obstáculos, com base nas escolhas do utilizador.
    De seguida, Cria a janela da implementação e desenha os objetos e sujidades
    (caso estas tenham sido fornecidas).
    Finalmente, cria o robot e corre-o no modo de terceira
    implementação. Quando o utilizador dá a ordem de regressar ao menu, fecha a
    janela da terceira implementação e termina o programa (corrido como
    subprocess a partir do main.py).
    """

    while True:
        TABLE_RADIUS, CHAIR_SIDE, WAITER_RADIUS, WAITER_SPEED, SHOW_GRID, \
            SHOW_CLEANED, DOCKING_RADIUS, TOLERANCE = get_settings()
        dirty_places, temp_win_size = menu_interpretation(WAITER_RADIUS, 
                                        CHAIR_SIDE,DOCKING_RADIUS, TABLE_RADIUS)
        if dirty_places == "quit": #Caso o utilizador feche os menus de escolha de modo de geração de sujidade ou obstáculos, termina a implementação
            break
        if temp_win_size is not None: #Caso o utilizador opte por obter os obstáculos a partir do ficheiro, as dimensões da janela serão as indicadas no ficheiro
            win_size = temp_win_size
        win = window_generator( WAITER_RADIUS,  win_size)
        if len(docking_stations) == 0: #Caso a localização das docking stations não tenha sido especificada, gera duas nos cantos da janela
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
    """Para evitar que o código seja corrido automaticamente caso este módulo seja
    importado, define-se que este só será corrido caso o módulo seja corrido 
    diretamente.
    """

    third_implementation()
    exit()
