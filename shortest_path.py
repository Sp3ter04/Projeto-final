# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from queue import PriorityQueue
from graphics import *
from universal_functions import *
from random import randint

"""Para identificar o caminho mais curto para qualquer ponto da sala, o robot 
utiliza o algoritmo A* - um dos algoritmos mais populares de pesquisa de caminhos
mais curtos entre dois nós de um grafo.
Para o fazer, o robot cria uma grelha com quadrículas que têm de lado metade do 
seu raio. A cada quadrícula, corresponde um nó no grafo e cada nó tem ligações a
todos os que lhe são imediatamente adjacentes. Os nós com posições relativas verticais 
e horizontais, têm entre si ligações de peso 1. Os que, por outro lado, têm posições 
relativas diagonais, estabelecem entre si ligações de peso 1.4 (esta distinção é
necessária numa grelha ortogonal porque, caso todas as ligações tivessem peso 1,
o robot favoreceria o movimento diagonal em relação ao horizontal e vertical e 
andaria aos ziguezagues).
Tendo um ponto inicial (localização atual do robot) e um ponto final (local para
onde o robot se quer deslocar), o robot executa o seguinte algoritmo para encontrar
o caminho mais curto entre os dois pontos:
Começando do nó inicial, o robot cria, para cada um dos seus nós adjacentes, uma
função f(n) = h(n) + g(n), sendo 'n' o nó em análise; h(n) o valor da soma de todas
as ligações percorridas a partir do nó principal até alcançar o nó 'n' e g(n) a 
estimativa mais otimista da distância entre o nó 'n' e o nó
final - ou seja, a distância 'boston' sem sesvios (foi utilizada a distância boston
 - dx + dy - em vez da distância em linha reta - sqrt(dx**2 + dy**2) - para simplificar
 o cálculo do valor de distância). 
Todos os pontos para os quais se calcula f(n) são adicionados ao open_set (uma 
priority queue - dessa forma, torna-se simples selecionar o próximo nó a analizar)
e, do open_set, é escolhido o nó com o menor valor de f(n) mais baixo para analizar
todos os seus nós adjacentes e repetir o processo.
Ao criar a grelha, o robot determina que células da grelha interceptam obstáculos,
para que, ao correr o algoritmo, os nós correspondentes a essas células nunca sejam
adicionados ao open_set e, portanto, nunca sejam considerados um caminho viável 
para o ponto destino. Desta forma, o robot consegue identificar, com um erro mínimo,
o caminho para qualquer ponto da sala, evitando sempre colisões com obstáculos.
"""

class Spot:
    """Cria o nó correspondente a cada um dos quadrados da grelha"""
    def __init__(self, row, col, cell_width, num_rows):
        """Para cada nó criado, definem-se as principais caraterísticas.
        
        A largura da célula, coordenadas na janela e na grelha, conjunto de 
        vizinhos, estado, forma, estado de limpeza e ponto âncora são atributos 
        aplicáveis a todas as células da grelha.
        """
        
        self.width = cell_width
        self.row = row #Coordenadas na grelha
        self.col = col
        self.num_rows = num_rows #Dimensão da grelha
        self.x_coord = col*self.width #Coordenadas na janela
        self.y_coord = row*self.width
        self.neighbors = [] #Conjunto dos nós a que está ligado
        self.state = "unchecked" 
        self.clean = False #utilizado na segunda e terceira implementação paara determinar onde o robot ainda não passou
        self.anchor = Point(self.x_coord, self.y_coord)
        self.shape = "square"

    def get_coords(self):
        """Devolve as coordenadas da célula."""
        return self.row, self.col
        
    def obstacle_spot(self):
        """Altera o atributo 'state' para obstáculo"""
        self.state = "obstacle"

    def ask_obstacle(self):
        """Retorna True se o 'state' fôr obstáculo. Caso contrário, retorna False."""
        return self.state == "obstacle"
        
    def reset(self):
        """Altera o atributo 'state' para não verificado"""
        self.state = "unchecked"

    def ask_limit(self, border_precision):
        """Retorna True se a célula estiver na periferia da janela. 
        
        A border precision permite que haja diferente tolerância à proximidade
        da periferia, consoante a implementação. Retorna False por defeito.
        """
        
        if self.x_coord < border_precision or self.x_coord >= 100 - border_precision:
            return True
        elif self.y_coord < border_precision or self.y_coord >= 100 - border_precision:
            return True
        else:
            return False 

    def get_square(self, win, outline):
        """Desenha na janela o outline da célula.
        
        Utilizado para mostrar a grelha ou mostrar a área limpa. Durante o 
        desenvolvimento, foi criado para fazer debugging do algoritmo.
        """
        
        self.square = Rectangle(Point(self.x_coord, self.y_coord), 
                           Point(self.x_coord + self.width, self.y_coord + self.width))
        self.square.setOutline(outline)
        self.square.draw(win)
        
    def check_over(self, grid):
        """Verifica os três nós 'vizinhos' superiores.
        
        Caso o vizinho em questão não intercepte obstáculo nenhum, é adicionado à 
        lista dos vizinhos do nó atual.
        """
        
        if self.row < self.num_rows - 1 \
                and not grid[self.row + 1][self.col].ask_obstacle(): #Vizinho imediatamente superior
            self.neighbors.append(grid[self.row + 1][self.col])
            if self.col < self.num_rows - 1 \
                    and not grid[self.row + 1][self.col + 1].ask_obstacle() \
                    and not grid[self.row][self.col + 1].ask_obstacle(): #Vizinho diagonal superior direito
                self.neighbors.append(grid[self.row + 1][self.col + 1])
                self.diagonal_neighbors.append(
                    grid[self.row + 1][self.col + 1])
            if self.col > 0 \
                    and not grid[self.row + 1][self.col - 1].ask_obstacle() \
                    and not grid[self.row][self.col - 1].ask_obstacle(): #Vizinho diagonal superior esquerdo
                self.neighbors.append(grid[self.row + 1][self.col - 1])
                self.diagonal_neighbors.append(
                    grid[self.row + 1][self.col - 1])
                
    def check_under(self, grid):
        """Verifica os três nós 'vizinhos' inferiores.
        
        Caso o vizinho em questão não intercepte obstáculo nenhum, é adicionado à 
        lista dos vizinhos do nó atual.
        """

        if self.row > 0 \
                and not grid[self.row - 1][self.col].ask_obstacle(): #Vizinho imediatamente inferior
            self.neighbors.append(grid[self.row - 1][self.col])
            if self.col < self.num_rows - 1 \
                    and not grid[self.row - 1][self.col + 1].ask_obstacle() \
                    and not grid[self.row][self.col + 1].ask_obstacle(): #Vizinho diagonal inferior direito
                self.neighbors.append(grid[self.row - 1][self.col + 1])
                self.diagonal_neighbors.append(
                    grid[self.row - 1][self.col + 1])
            if self.col > 0 \
                    and not grid[self.row - 1][self.col - 1].ask_obstacle() \
                    and not grid[self.row][self.col - 1].ask_obstacle(): #Vizinho diagonal inferior esquerdo
                self.neighbors.append(grid[self.row - 1][self.col - 1])
                self.diagonal_neighbors.append(
                    grid[self.row - 1][self.col - 1])
                
    def check_left(self, grid):
        """Verifica o vizinho da esquerda.
        
        Caso não intercepte nenhum obstáculo, adiciona-o à lista dos vizinhos.
        """
        
        if self.col > 0 \
                and not grid[self.row][self.col - 1].ask_obstacle(): 
            self.neighbors.append(grid[self.row][self.col - 1])

    def check_right(self, grid):
        """Verifica o vizinho da direita.
        
        Caso não intercepte nenhum obstáculo, adiciona-o à lista dos vizinhos.
        """

        if self.col < self.num_rows - 1 \
                and not grid[self.row][self.col + 1].ask_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])

    def update_neighbors(self, grid):
        """Coordena as rotinas de verificação de todos os vizinhos"""
        self.neighbors = []
        self.diagonal_neighbors = []
        self.check_over(grid)
        self.check_under(grid)
        self.check_left(grid)
        self.check_right(grid)


    def check_occupation(self, obstacle_list, win, chair_precision, table_precision, border_precision):
        """Verifica, para a célula atual, se há intercepção com algum dos obstáculos"""
        occupation = []
        if self.ask_limit(border_precision): #Se estiver na periferia, é dado como obstáculo
            occupation.append("limit")
        else:
            for obstacle in obstacle_list: 
                """Itera a lista dos obstáculos e verifica se qualquer deles 
                intercepta a célula (aplicando o algoritmo de deteção adequado à sua forma)
                
                """
                if obstacle.shape == "square":
                    if square_square_interception((self.x_coord, self.y_coord), self.width,
                                                (obstacle.anchor.getX(), obstacle.anchor.getY()), 
                                                obstacle.width, chair_precision):
                        occupation.append(obstacle)
                elif obstacle.shape == "circle":
                    if circle_square_interception((self.x_coord, self.y_coord), self.width, 
                                                (obstacle.anchor.getX(), obstacle.anchor.getY()), 
                                                obstacle.radius, table_precision):
                        occupation.append(obstacle)
                    
        if len(occupation) != 0: #Caso algum obstáculo intercepte a célula, o 'status' passa a ser obstáculo
            self.obstacle_spot()
            
                        
        
def grid_maker(window_size, cell_width):
    """Cria a grelha para sobrepôr à janela.
    
    A grelha tem uma dimensão dependente das dimensões da janela e do raio do 
    robot. Devolve a grelha.
    """
    
    cell_width = cell_width
    num_rows = window_size // cell_width
    grid = []
    for row in range(int(num_rows)):
        grid.append([]) 
        for col in range(int(num_rows)):
            spot = Spot(row, col, cell_width, num_rows) #Cria um objeto da classe Spot para cada célula da grelha
            grid[row].append(spot)
    return grid


def g_value(p_A, p_B):
    """Devolve a distância 'boston' entre o ponto atual (p_A) e o ponto final (p_B)."""
    x_A, y_A = p_A
    x_B, y_B = p_B
    g_value = abs(x_A - x_B) + abs(y_A - y_B)
    return g_value

def algorithm(grid, start, end):
    """Determina o caminho mais curto entre o ponto inicial e o ponto final.
    
    Recebe a grelha, o ponto inicial e o ponto final e executa o algoritmo A*, tal
    como descrito em detalhe no início do ficheiro.
    """
    
    count = 0 #Utilizado para desempate caso dois pontos tenham um valor de f(n) igual
    open_set = PriorityQueue() #Cria a lista de pontos analisados
    open_set.put((0, count, start)) #Adiciona o ponto inicial à lista
    came_from = {} #Utilizado para calcular h(n)
    h_value = {spot: float("inf") for row in grid for spot in row} #Todos as células começam com um valor de h(n) infinito, para garantir que são analisadas pela ordem pretendida
    h_value[start] = 0
    f_value = {spot: float("inf") for row in grid for spot in row} #O valor inicial de f(n) infinito garante que a prioridade no open_set é dada aos nós corretos
    open_set_copy = {start} #Permite manter um registo das operações realizadas ao open_set
    while not open_set.empty():
        """Corre o algoritmo até chegar ao ponto final"""
        current = open_set.get()[2]
        open_set_copy.remove(current)
        if current == end: #Chegando ao ponto final, termina o algoritmo e devolve o caminho mais curto
            path_to_dirt = []
            while current in came_from: #Identifica o caminho percorrido desde o ponto inicial até ao final
                current = came_from[current]
                path_to_dirt.insert(0, current)
            return path_to_dirt
        for neighbor in current.neighbors: #Atualiza os valores de h(n) de todos os vizinhos do nó atual
            if neighbor not in current.diagonal_neighbors:
                temp_h_value = h_value[current] + 1
            else:
                temp_h_value = h_value[current] + 1.4
            if temp_h_value < h_value[neighbor]:
                came_from[neighbor] = current
                h_value[neighbor] = temp_h_value
                f_value[neighbor] = temp_h_value + \
                    g_value(neighbor.get_coords(), end.get_coords())
                if neighbor not in open_set_copy:
                    count += 1
                    open_set.put((f_value[neighbor], count, neighbor))
                    open_set_copy.add(neighbor)


def get_spot(point, cell_width):
    """Devolve as coordenadas da célula da grelha correspondente ao ponto."""
    spot_width = cell_width
    x, y = point[0], point[1]
    row = int(y // spot_width)
    col = int(x // spot_width)
    return row, col

def initialize_algorithm(cell_width, obstacle_list, win, chair_precision=0, table_precision=0, border_precision=0):
    """Cria a grelha e verifica quais das células interceptam obstáculos.
    
    Devolve duas grelhas: uma que inclui as células-obstáculo e outra que não inclui
    as células-obstáculo (utilizada na segunda e terceira implementação).
    """
    
    grid = grid_maker(100, cell_width)
    for row in grid:
        for spot in row:
            spot.check_occupation(obstacle_list, win, chair_precision, table_precision, border_precision)
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
    non_obstacle_grid = non_obstacle_gridmaker(grid)
    return grid, non_obstacle_grid


def non_obstacle_gridmaker(grid):
    """Cria a grelha sem obstáculos.
    
    De quatro em quatro linhas, a ordem de adição das células à grelha é trocada, 
    uma vez que o robot ocupa e tem capacidade de limpar quatro linhas de uma vez.
    Desta maneira, atinge-se maior eficiência, continuando o robot a cobrir toda
    a área da sala.
    """
    
    turn = 1
    count = 0
    non_obstacle_grid = []
    for row in grid:
        non_obstacle_grid.append([])
        for spot in row:
            if not spot.ask_obstacle():
                if turn > 0:
                    non_obstacle_grid[grid.index(row)].append(spot)
                else:
                    non_obstacle_grid[grid.index(row)].insert(0, spot)
        if count % 4:
            turn *= -1
        count += 1
    return non_obstacle_grid
    

def run_algorithm(cell_width, grid, start_point, end_point): 
    """Coordena todas as funções necessárias para correr o algoritmo.
     
    Devolve o caminho mais curto.
    """
    
    row_start, col_start = get_spot(start_point, cell_width)
    row_end, col_end = get_spot(end_point, cell_width)
    start = grid[row_start][col_start]
    end = grid[row_end][col_end]
    path_to_dirt = algorithm(grid, start, end)
    return path_to_dirt
