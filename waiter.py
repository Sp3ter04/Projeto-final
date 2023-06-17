# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from math import cos, sin
from shortest_path import *
from universal_functions import *
from obstacles import *
from button import Button

LED_GREEN = color_rgb(17, 207, 48) #Define as cores do led da bateria
LED_BLUE = "blue"
LED_RED = "red"
class Waiter:
    """Cria a classe waiter - classe do robot.
    
    Waiter tem duas subclasses: Waiter1 e Waiter23, utilizadas alternativamente 
    consoante a implementação que vai ser corrida.
    """
    
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid):
        """É gerado o robot.
        
        O robot tem atributos correspondentes às suas caraterísticas físicas,
        bem como aos detalhes necessários para o seu funcionamento.
        """
        
        self.show_grid = show_grid
        self.win = win
        self.radius = radius
        self.docking_stations = docking_stations
        self.anchor = self.docking_stations[0].anchor
        self.tolerance = tolerance
        self.speed = speed
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(41, 39, 39))
        self.outline = Circle(self.anchor, self.radius * 0.95)
        self.outline.setFill("gray")
        self.quit = False
        self.start = False
        self.cell_width = self.radius / 2
        self.battery = 9500 #A bateria tem um valor inicial de 9500 - obtido fazendo a média dos gastos de bateria na segunda e terceira implementação
        self.body_entities = [self.body, self.outline] #Conjunto de entidades do 'corpo' do robot desenhadas na janela
        self.get_buttons() #cria um botão 'start' e outro 'exit'

    def grid_show(self):
        """Mostra a grelha, se essa opção for selecionada."""
        if self.show_grid:
            for row in self.grid:
                for spot in row:
                    if spot.ask_obstacle():
                        spot.get_square(self.win, "black")

    def get_buttons(self):
        """Cria os botões e desenha-os na janela."""
        self.start_button = Button(Point(3, 97.5), Point(
            11, 100), color_rgb(41, 39, 39), color_rgb(184, 162, 125), 
            "Start", color_rgb(41, 39, 39), 13)
        self.quit_button = Button(Point(0, 97.5), Point(3, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", 
            color_rgb(41, 39, 39), 13)
        self.buttons = [self.start_button, self.quit_button]
        for button in self.buttons:
            button.body.setWidth(1)
            button.draw(self.win)

    def draw(self):
        """Desenha todas as entidades incluídas na lista de body_entities."""
        for entity in self.body_entities:
            entity.draw(self.win)

    def undraw(self):
        """Retira da janela todas as entidades da lista body_entities."""
        for entity in self.body_entities:
            entity.undraw()

    def get_dirty_spots(self):
        """Obtém uma lista de pontos sujos, caso nenhum botão seja pressionado.
        
        Recolhe o clique do utilizador. Caso o botão de sair tenha sido pressionado,
        termina a implementação. Se o botão pressionado tiver sido o 'start', corre
        a implementação com a lista de pontos sujos atual. Caso o ponto clicado 
        esteja fora dos botões, verifica se o ponto é alcançável. Caso o seja, 
        cria um ponto de maior sujidade nesse local. Caso contrário, apresenta
        uma mensagem de erro, indicando ao utilizador que a sujidade não deve
        interceptar obstáculos.
        """
        
        dirty_spots = []
        while not self.start:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                    for spot in dirty_spots:
                        spot.cleaned()
                    self.quit = True
                    break
            if self.start_button.clicked(mouse_click):
                self.start = True
            else: #Corre o algoritmo para verificar se existe um caminho disponível para o ponto
                path_to_dirt = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(), 
                                            self.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()))
                if path_to_dirt == None: #Se não existir caminho nenhum para o ponto, mostra a mensagem de erro
                    display_error_message("O ponto sujo não pode \n interceptar obstáculos", self.win)
                    continue
                dirt = Dirt(mouse_click, self, self.win)
                dirty_spots.append(dirt)
        return dirty_spots
    
    def move_with_shortest_path(self, target, dirty_spots=[]):
        """Identifica o caminho mais curto para o ponto e percorre-o."""
        path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(),
            self.body.getCenter().getY()), (target.getX(), target.getY())) #Encontra o caminho mais curto
        for point in path: #Até atingir o destino, itera a lista de pontos no caminho
            if len(dirty_spots) > 0:
                if self.collision(dirty_spots):
                    return_spot = self.body.getCenter()
                    spot = self.latest_collision
                    self.move(spot.body.getCenter())
                    self.clean_spot()
                    dirty_spots.remove(spot)
                    spot.cleaned()
                    self.move(return_spot)
            self.move(Point(point.x_coord + self.radius /
                            4, point.y_coord + self.radius / 4))
        self.move(target) #Atingindo a célula final da grelha, dirige-se às coordenadas precisas do ponto-destino
    
    def move(self, target):
        """Move o robot de um ponto para outro.
        
        Começa por calcular o versor do movimento e desloca-se, posteriormente,
        nessa direção até atingir o ponto-alvo. A velocidade do movimento é um 
        atributo do robot.
        """
        
        dx, dy = self.get_vector(target)
        while self.continue_moving(target):
            self.battery -= 1 #cada vez que se move, a bateria perde 1 unidade
            for entity in self.body_entities:
                entity.move(dx, dy)
            update(self.speed)

    def get_vector(self, target):
        """Calcula o versor do movimento entre o ponto atual e o ponto-objetivo."""
        delta_x, delta_y, distance = get_distance(
            target, self.body.getCenter())
        dx = delta_x / (distance * 2.5 + 0.01) #caso os pontos estejam sobrepostos, para evitar a divisão por 0, adiciona-se 0.01 à discância
        dy = delta_y / (distance * 2.5 + 0.01)
        return dx, dy #Retorna as coordenadas do versor

    def continue_moving(self, target):
        """Determina se o robot atingiu o destino.
        
        Uma vez que o movimento não tem um versor infinitesimal, é necessário
        estabelecer uma tolerância a partir da qual se considera que o robot atingiu
        o ponto-objetivo. Caso contrário, frequentemente o robot ficaria preso num
        ciclo infinito de movimento sem nunca atingir o ponto.
        """
        
        distance = get_distance(target, self.body.getCenter())[2]
        if not int(distance*10) in range(int(self.tolerance*10)):
            return True
        else:
            return False

    def clean_spot(self):
        """Chegando ao ponto sujo, o robot limpa-o num movimento em espiral."""
        dirt_center = self.body.getCenter()
        theta = 0
        spiral = 0
        while spiral < 0.4 * self.radius: #Faz um movimento aproximadamente expiral, incrementando o ângulo e o raio gradualmente
            x = dirt_center.getX() + spiral * cos(theta)
            y = dirt_center.getY() + spiral * sin(theta)
            dx = x - self.body.getCenter().getX()
            dy = y - self.body.getCenter().getY()
            for entity in self.body_entities:
                entity.move(dx, dy)
            theta += 0.30
            spiral += 0.02
            update(self.speed / 2.5)
        

    def move_to_docking(self):
        """Move-se para a docking-station mais próxima.
        
        Avalia o tamanho do caminho mais curto para todas as docking stations e,
        determinando para qual delas o caminho é menor, dirige-se para essa.
        """
        
        station_paths = {}
        path_sizes = []
        for station in self.docking_stations:
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(), 
                                self.body.getCenter().getY()), (station.anchor.getX(), station.anchor.getY()))
            station_paths.update({station : path})
        try:
            for path in station_paths.values():
                path_sizes.append(len(path))
        except: #Caso uma ou mais docking stations se encontrem inacessíveis, evita o erro e continua a correr o programa
            pass
        shortest_index = path_sizes.index(min(path_sizes))
        for point in list(station_paths.values())[shortest_index]:
            self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))
        self.move(self.docking_stations[shortest_index].anchor)

    def collision(self, entity_list, tolerance=0):
        """Determina se o robot está a interceptar alguma das entidades na lista."""
        collisions = []
        for entity in entity_list:
            ent = (entity.anchor.getX(), entity.anchor.getY())
            waiter = (self.body.getCenter().getX(), self.body.getCenter().getY())
            if entity.shape == "square": #Escolhe o modo adequado de deteção de intercepções 
                if circle_square_interception(ent, entity.width, waiter, self.radius, tolerance):
                    collisions.append(entity)
            elif entity.shape == "circle":
                if circle_circle_interception(ent, entity.radius, waiter, self.radius, tolerance):
                    collisions.append(entity)
        if len(collisions) != 0: #Caso haja colisão, retorna True
            self.latest_collision = collisions[len(collisions) - 1]
            return True
        else: #Caso não intercepte nenhuma das entidades, retorna False
            return False




class Waiter1(Waiter):
    """Cria um robot com os métodos necessários para correr a primeira implementação."""
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid):
        super().__init__(radius, tolerance, speed, docking_stations, win, show_grid)
        """Gera robot da primeira implementação.
        
        Este robot cria uma grelha com uma tolerância para a distância aos 
        obstáculos maior do que a requerida para a segunda e terceira implementação.
        """
        
        self.grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 2.7, self.cell_width * 1.3, self.cell_width * 2)[0]
        self.grid_show()
        self.draw()


        
    def clean_dirty_spots(self, dirty_spots):
        """Itera a lista de pontos sujos e dirige-se a cada um.
        
        Dirige-se aos pontos sujos pela ordem em que estes foram introduzidos pelo
        utilizador. Chegando a um ponto, executa a rotina de limpeza e altera o
        seu estado para limpo.
        """
        
        for spot in dirty_spots:
            spot_center = spot.body.getCenter()
            self.move_with_shortest_path(spot_center)
            self.clean_spot()
            spot.cleaned()



    def clean_room(self):
        """Corre a primeira implementação.
        
        Começa por recolher o clique do utilizador e determinar se este corresponde
        a um botão pressionado (reage em concordância, nessa situação) ou, não 
        correspondendo, se é um sítio válido para a introdução de um ponto sujo.
        Caso o botão de sair seja pressionado, termina a implementação. Caso o 
        botão 'start' seja pressionado, executa a rotina de limpeza. Se o ponto 
        fôr válido para introduzir um ponto de maior sujidade, caso nenhum botão
        tenha sido pressionado, cria um ponto sujo nesse local.
        """
        
        while True:
            dirty_spots = self.get_dirty_spots()            
            if not self.quit:
                self.clean_dirty_spots(dirty_spots)
                self.move_to_docking()
                self.start = False
            else: #Caso o utilizador escolha sair do programa, os obstáculos são eliminados da janela e o ciclo é quebrado
                for obstacle in obstacle_list:
                    obstacle_list.remove(obstacle)
                break



class Waiter23(Waiter):
    """Cria o robot utilizado na segunda e terceira implementação."""
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid, show_cleaned, dirty_places=[]):
        """Gera o robot da implementação 2 e 3.
        
        Depois de gerado o restaurante, a segunda e terceira implementação correm
        exatamente da mesma forma: o robot percorre toda a sala, limpando os pontos
        de maior sujidade quando se cruza com eles. Se, durante o percurso, ficar 
        sem bateria, dirige-se a uma docking station para carregar (o led muda de 
        cor). Depois do carregamento, retoma o percurso.
        """

        super().__init__(radius, tolerance, speed, docking_stations, win, show_grid)
        self.dirty_places = dirty_places
        self.show_cleaned = show_cleaned
        self.grid, self.non_obstacle_grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 2, self.cell_width * 2) #A grelha tem tolerâncias menores que na primeira implementação
        self.grid_show()
        self.latest_collision = None
        self.charge_led = Circle(self.body.getCenter(), self.radius * 0.35) #Cria o led da bateria
        self.charge_led.setFill(LED_GREEN)
        self.body_entities.append(self.charge_led)
        self.draw()

    def get_dirt_from_file(self):
        """Cria os pontos sujos retirados do ficheiro.
        
        Caso o utilizador tenha optado por obter os pontos sujos a partir do 
        ficheiro, esta rotina converte os placeholders em pontos sujos reais.
        Com o robot já criado, itera pela lista dos sítios sujos e cria pontos
        de maior sujidade reais, desenhando-os na janela.
        """
        
        dirty_spots = []
        for dirt in self.dirty_places:
            dirty_spots.append(Dirt(dirt.anchor, self, self.win))
        while not self.start: #Verifica se foi pressionado o botão de sair ou o botão 'start'
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                for spot in dirty_spots:
                    spot.cleaned()
                self.quit = True
                break
            if self.start_button.clicked(mouse_click):
                self.start = True
        return dirty_spots #Retorna os pontos sujos

    def low_battery(self):
        """Dirige-se a uma docking station para carregar (muda as cores do led)."""
        return_pos = self.body.getCenter()#Guarda o ponto em que se encontrava
        self.charge_led.setFill(LED_RED)
        self.move_to_docking()
        self.charge_led.setFill(LED_BLUE)
        time.sleep(2) #Espera dois segundos na docking station até retomar a limpeza
        self.battery = 9500 #Repõe a carga da bateria
        self.charge_led.setFill(LED_GREEN)
        self.move_with_shortest_path(return_pos)#Retorna ao ponto onde se encontrava antes da rotina de carregamento

    def clean_whole_room(self):
        """Corre a segunda / terceira implementação.
        
        Identifica, primeiro, se o utilizador optou por sujidades lidas do ficheiro.
        Caso tenha optado, cria as sujidades a partir do ficheiro. Caso contrário,
        recolhe cliques do utilizador para criar pontos sujos, até que este pressione
        o botão de saída ou o botão 'start'. Caso o botão de saída tenha sido 
        pressionado, termina a implementação. Caso o botão 'start' seja pressionado,
        inicia a rotina de limpeza.
        """
        
        while True:
            if len(self.dirty_places) != 0:
                dirty_spots = self.get_dirt_from_file()
            else:
                dirty_spots = self.get_dirty_spots()
            if not self.quit:
                for row in self.non_obstacle_grid:
                    for spot in row:
                        spot.clean = False
                self.move_through_grid(dirty_spots)
                self.move_to_docking()
                self.start = False
            else:
                for obstacle in obstacle_list:
                    obstacle_list.remove(obstacle)
                break

    
    def move_through_grid(self, dirty_spots):
        """Rotina de limpeza.
        
        Passa por todos os pontos da grelha que não tenham obstáculo, mudando o 
        seu estado para limpo quando o faz. Ao colidir com um ponto sujo, limpa 
        o ponto, retomando, depois, o seu caminho. Caso a bateria fique demasiado 
        baixa, dirige-se à docking station para a carregar.
        """
        
        for row in self.non_obstacle_grid[3::4]:#Seleciona as linhas da grelha a visitas - o robot ocupa quatro linhas
            for spot in row: #Itera por todas as células da grelha, determinando quais ainda não foram limpas
                for neighbor in spot.neighbors:
                    for second_neighbor in neighbor.neighbors:
                        if self.collision([second_neighbor]): 
                            second_neighbor.clean = True
                            if self.show_cleaned: #Caso o modo show_cleaned esteja ativado, ao limpar uma célula torna o seu outline azul, tornando a área limpa visível
                                square = second_neighbor.get_square(self.win, "blue")
                if not spot.clean:
                    spot_anchor = (spot.anchor.getX(), spot.anchor.getY())
                    target = Point(
                        spot_anchor[0] + self.cell_width/2, spot_anchor[1] + self.cell_width/2)
                    if self.battery <= 250: #Determina se a bateria está fraca
                        self.low_battery()
                    try:
                        self.move_with_shortest_path(target, dirty_spots)
                    except:
                        continue


