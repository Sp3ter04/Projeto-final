# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from random import randint

obstacle_list = []
docking_stations = []

class Obstacle:
    """Classe mãe das classes de obstáculos.
    
    Tem duas classes filhas: Chair e Table"""
    def __init__(self, anchor):
        """Cria um obstáculo.
        
        O parâmetro anchor é um tuple com as coordenadas do ponto âncora do obstáculo.
        Ao ser criado, o obstáculo é imediatamente adicionado à lista de 
        obstáculos.
        """
        
        self.anchor = Point(anchor[0], anchor[1])
        obstacle_list.append(self)

    def draw(self, win):
        """Desenha o obstáculo.
        
        A lista body_entities contém a totalidade dos elementos do
        obstáculo que serão visíveis na janela do programa.
        """

        for entity in self.body_entities:
            entity.draw(win)



class Table(Obstacle):
    """Cria uma mesa na janela da implementação."""
    def __init__(self, anchor, radius):
        """Gera uma mesa.
        
        Além do parâmetro anchor, herdado da classe obstáculo, recebe também um 
        radius, que vai corresponder ao raio da mesa.
        Ao ser criada, a mesa adquire um atributo - a lista body_entities -
        correspondente ao conjunto das entidades que serão desenhadas na janela.
        O atributo body corresponde à forma simples (circular) da mesa - objeto
        da calsse Circle do módulo graphics.py. O body será o atributo utilizado
        em todos os cálculos relativos à posição da mesa.
        Tal como as outras peças de mobília, a mesa tem um atibuto shape, neste
        caso de valor "circle", que será utilizado para escolher o algoritmo do 
        cálculo de intersepções.
        """
        
        super().__init__(anchor)
        self.radius = radius
        self.shape = "circle"
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(82, 96, 112))
        self.body_entities = [self.body]
        self.get_decorations()

    def get_decorations(self):
        """Coordena a criação das decorações da mesa."""
        self.get_towel(self.radius * 0.72, "white")
        self.get_towel(self.radius * 0.67, color_rgb(82, 96, 112))
        self.get_towel(self.radius * 0.50, color_rgb(254, 220, 86))
        self.get_towel(self.radius * 0.45, color_rgb(82, 96, 112))
        self.get_dishes()

    def get_dishes(self):
        """Cria os quatro pratos visíveis na mesa
        
        Cada prato tem um raio e uma posição fixa em relação ao centro e
        dimensões da mesa. Para criar os pratos, começa por gerar os seus pontos
        âncora, criando, em seguida, os pratos e adicionando-os à lista dishes.
        Finalmente, iterando a lista dishes e, para cada um dos seus elementos,
        iterando as entidades que o constituem, adiciona todas as novas
        entidades à lista body_entities. 
        """
        
        dish_radius = self.radius * 0.3
        dishes = []
        point1 = Point(self.anchor.getX() + self.radius * 0.65, self.anchor.getY())
        point2 = Point(self.anchor.getX() - self.radius * 0.65, self.anchor.getY())
        point3 = Point(self.anchor.getX(), self.anchor.getY() + self.radius * 0.65)
        point4 = Point(self.anchor.getX(), self.anchor.getY() - self.radius * 0.65)
        for point in [point1, point2, point3, point4]:
            dishes.append(self.construct_dish(point, dish_radius))
        for dish in dishes:
            for entity in dish:
                self.body_entities.append(entity)
        

    def construct_dish(self, anchor, radius):
        """Cria cada um dos pratos.
        
        Recebe um ponto âncora e um raio e cria um prato (constituído por dois
        círculos concêntricos). No fim, devolve o prato criado.
        """
        
        outer_circle = Circle(anchor, radius)
        outer_circle.setFill("white")
        inner_circle = Circle(anchor, radius * 0.75)
        inner_circle.setFill(color_rgb(250, 249, 254))
        dish = [outer_circle, inner_circle]
        return dish

    def get_towel(self, radius, color):
        """Cria uma toalha para a mesa.
        
        A toalha é um objeto da classe Circle do módulo graphics.py, com um raio
        e uma cor que são parâmetros da função. Depois de criada a toalha, 
        adiciona-a às body entities.
        """
        
        towel = Circle(self.anchor, radius)
        towel.setFill(color)
        self.body_entities.append(towel)

class Chair(Obstacle):
    """Cria uma cadeira na janela da implementação."""
    def __init__(self, anchor, width):
        """Gera a cadeira.
        
        Além do parâmetro anchor, herdado da classe Obstacle, recebe também um
        parâmetro width, correspondente ao lado da cadeira.
        
        Ao ser criada, a cadeira adquire uma lista body_entities, que contém todas 
        as entidades que serão desenhadas na janela da implementação.
        A única decoração necessária na cadeira é um buraco no seu centro, que é
        obtido através do método get_hole.
        Tal como as outras peças de mobília, a cadeira tem um atibuto shape, 
        neste caso de valor "square", que será utilizado para escolher o 
        algoritmo do cálculo de intersepções.
        """
        
        super().__init__(anchor)
        self.width = width
        self.shape = "square"
        self.p2 = Point(anchor[0] + self.width, anchor[1] + self.width)
        self.hole = self.get_hole()
        self.body = Rectangle(self.anchor, self.p2)
        self.body.setFill(color_rgb(184, 162, 125))
        self.body_entities = [self.body, self.hole]

    def get_hole(self):
        """Cria o buraco no centro da cadeira.
        
        O buraco é um objeto da classe Circle, com um atributo setFill da mesma
        cor da carpete.
        """
        
        center = Point(self.anchor.getX() + self.width / 2, self.anchor.getY() + self.width / 2)
        hole = Circle(center, self.width * 0.15)
        hole.setFill(color_rgb(217, 202, 165))
        return hole

class Docking:
    """Cria uma docking station."""
    def __init__(self, anchor, radius):
        """Gera a docking station.
        
        A partir do ponto âncora e do raio (parâmetros), cria uma caixa quadrada
        com uma zona circular circunscrita à qual o robot se dirige entre 
        utilizações, ou quando necessita de carregar.
        A lista body_entities contém todos os elementos da docking station que 
        serão desenhados na janela.
        O atributo shape, tal como em qualquer outra peça de mobília, é utilizado
        para cálculo de intercepções. Neste caso, tem um valor "circle".
        """
        docking_stations.append(self)
        self.anchor = Point(anchor[0], anchor[1])
        self.shape = "circle"
        self.radius = radius
        self.box = self.get_box()
        self.inner_circle = Circle(self.anchor, radius * 0.92)
        self.inner_circle.setFill(color_rgb(65, 66, 69))
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(82, 96, 112))
        self.body_entities = [self.box, self.body, self.inner_circle]

    def get_box(self):
        """Cria a caixa exterior da docking station.
        
        Os pontos point1 e point2 são os cantos inferior-esquerdo e 
        superior-direito da caixa. A box é um objeto da classe Rectangle.
        """

        point1 = Point(self.anchor.getX() - self.radius, self.anchor.getY() - self.radius)
        point2 = Point(self.anchor.getX() + self.radius,self.anchor.getY() + self.radius)
        box = Rectangle(point1, point2)
        box.setFill(color_rgb(41, 39, 39))
        return box

    def draw(self, win):
        """Desenha na janela todas as entidades na lista body_entities."""
        for entity in self.body_entities:
            entity.draw(win)

class DirtPlaceHolder:
    """Cria um placeholder para a sujidade.
    
    Um ponto sujo só pode ser criado depois de o waiter ter sido criado, pelo que,
    caso se opte, na terceira implementação, por sujidades lidas no ficheiro, se
    torna necessário criar uma entidade que "reserve" o espaço que será ocupado
    pela sujidade. Desta forma, se os obstáculos forem gerados aleatoriamente,
    é possível evitar que estes interceptem as sujidades do ficheiro.
    O placeholder tem apenas os atributos necessários para o cálculo de intercepções:
    anchor, radius e shape.
    """
    
    def __init__(self, anchor, waiter_radius):
        """Gera o placeholder da sujidade, com atributos anchor, radius e shape."""
        self.anchor = anchor
        self.radius = waiter_radius * 1.2
        self.shape = "circle"

class Dirt:
    """Cria um ponto de maior sujidade.
    
    Para efeitos decorativos, optou-se por conferir ao ponto sujo a aparência de
    um ovo estrelado. O ponto sujo tem uma zona exterior circular (branca),
    utilizada como referência em todos os cálculos relacionados com a sua 
    posição. No interior, há um círculo amarelo (representa a gema) que adquire 
    uma posição escolhida aleatoriamente de uma lista predefinida.
    """
    
    def __init__(self, anchor, waiter, win):
        """Gera o ponto sujo.
        
        O raio do ponto é sempre 120 % do raio do robot, uma vez que isso lhe
        confee uma área interior que é aproximadamente duas vezes a do robot.
        Tanto a clara (body), como a gema (yolk), são objetos da classe Circle.
        Para que o robot se sobreponha ao ponto sujo enquanto executa a rotina
        de limpeza, é necessário que seja desenhado na janela depois do ponto 
        sujo. Por essa razão, optou-se por incluir na função geradora da sujidade
        chamadas para os métodos undraw() e subsequentemente draw() do robot, 
        garantindo que este será sempre desenhado depois de qualquer sujidade 
        que seja adicionada à janela.
        """

        self.anchor = anchor
        self.radius = waiter.radius * 1.2
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(250, 249, 254))
        self.body_entities = [self.body]
        self.get_yolk()
        self.draw(win)
        self.shape = "circle"
        waiter.undraw() #retira o robot da janela
        waiter.draw() #desenha novamente o robot, agora sobreponde-se à sujidade

    def get_yolk(self):
        """Cria a gema.
        
        Começa por criar uma lista de posições em x e outra em y. Qualquer
        combinação de coordenadas x e y destas listas permite que o ponto sujo 
        ganhe a aparência de ovo estrelado (outras posições da gema não seriam 
        tão eficazes nessa função).
        Em seguida, cria um ponto (com coordenadas selecionadas aleatoriamente 
        das listas) e, a partir dele, cria a gema - objeto da classe Circle.
        Finalmente, adiciona a gema à lista de body_entities.
        """
        
        yolk_y_positions = [-0.18 * self.radius, 0, 0.18 * self.radius]
        yolk_x_positions = [-0.18 * self.radius, 0.18 * self.radius]
        center = Point(self.anchor.getX() + yolk_x_positions[randint(0, 1)], 
                       self.anchor.getY() + yolk_y_positions[randint(0, 2)])
        yolk = Circle(center, self.radius * 0.4)
        yolk.setFill(color_rgb(250, 129, 36))
        self.body_entities.append(yolk)

    def draw(self, win):
        """Desenha na janela todos os componentes do ponto sujo."""
        for entity in self.body_entities:
            entity.draw(win)

    def cleaned(self):
        """Apaga da janela todos os componentes do ponto sujo.
        
        Ese método é utilizado quando o robot acaba de limpar o ponto de maior 
        sujidade.
        """
        
        for entity in self.body_entities:
            entity.undraw()

