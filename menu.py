# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from universal_functions import *
from obstacles import *
from button import Button
from settings import *
import subprocess


class Menu:
    """Cria o menu principal, que aparece sempre que o programa é corrido."""
    def __init__(self):
        """Gera o menu principal.
        
        Gera uma janela, decora-a com docking stations, uma carpete e uma área 
        para os botões. Cria o título e as instruções de utilização, bem como os
        botões.
        """
        
        self.win = GraphWin("Menu", 800, 800)
        self.win.setCoords(0, 0, 100, 100)
        self.win.setBackground(color_rgb(61, 36, 1))
        self.get_decorations()
        self.get_text()
        self.get_buttons()
        for decoration in self.decorations:
            decoration.draw(self.win)
        for entity in self.text:
            entity.draw(self.win)
        for button in self.buttons:
            button.draw(self.win)


    def get_decorations(self):
        """Cria as decorações da janela do menu.
        
        Gera uma carpete, duas docking stations e a área dos botões.
        """

        self.carpet = Rectangle(Point(4, 4),
                        Point(96, 96))
        self.carpet.setFill(color_rgb(217, 202, 165))
        self.docking1 = Docking((4.8, 4.8), 4.8)
        self.docking2 = Docking((95.2, 95.2), 4.8)
        self.button_container = Rectangle(Point(8, 2.5), Point(92, 97.5))
        self.button_container.setFill(color_rgb(184, 162, 125))
        self.decorations = [self.carpet, self.docking1, self.docking2, self.button_container]

    def get_text(self):
        """Cria o texto visível no menu.
        
        Gera e caracteriza o texto para o título do programa e para as instruções
        de utilização.
        """

        self.title = Text(Point(50, 75), "Robô de Limpeza")
        self.title.setFace("times roman")
        self.title.setStyle("bold")
        self.title.setSize(30)
        self.title.setTextColor(color_rgb(65, 66, 69))
        self.instructions = Text(Point(50, 70), "Selecione a Implementação")
        self.instructions.setFace("times roman")
        self.instructions.setStyle("bold")
        self.instructions.setSize(18)
        self.instructions.setTextColor(color_rgb(65, 66, 69))
        self.text = [self.title, self.instructions]

    def get_buttons(self):
        """Cria os botões do menu.
        
        Gera três botões para as implementações - todos com o mesmo formato. Além
        disso, cria um botão para encerrar o programa e outro para as definições.
        """

        self.first_imp_button = Button(Point(20, 50), Point(80, 60), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Primeira Implementação", color_rgb(65, 66, 69), 13)
        self.second_imp_button = Button(Point(20, 35), Point(80, 45), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Segunda Implementação", color_rgb(65, 66, 69), 13)
        self.third_imp_button = Button(Point(20, 20), Point(80, 30), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Terceira Implementação", color_rgb(65, 66, 69), 13)
        self.quit_button = Button(Point(0, 96.5), Point(
            4, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", color_rgb(41, 39, 39), 13)
        self.quit_button.body.setWidth(1)
        self.settings_button = Button(Point(4, 96.5), Point(20, 100), color_rgb(250, 249, 254), color_rgb(217, 202, 165),
            "Definições", color_rgb(41, 39, 39), 13)
        self.settings_button.body.setWidth(2)
        self.buttons = [self.quit_button, self.settings_button, self.first_imp_button, self.second_imp_button, self.third_imp_button]

    def get_button_press(self):
        """Determina que botão foi pressionado pelo utilizador.
        
        Recolhe o clique do utilizador e determina qual dos botões foi pressionado.
        Caso tenha sido o de encerramento ou uma das implementações, devolve uma 
        string relacionada com a função do botão. Caso o botão pressionado tenha 
        sido o das definições, corre o menu das definições como subprocess. Se o
        clique do utilizador não interceptar nenhum dos botões, pede um novo 
        clique e repete o processo.
        """

        while True:
            """O loop permite que, até um botão ter sido pressionado, o programa
            continue a recolher o clique do utilizador. Além disso, permite manter
            o menu aberto enquanto o utilizador ajusta as definições e automatiza
            o retorno ao menu caso a janela das definições seja fechada.
            """

            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                return "quit"
            elif self.settings_button.clicked(mouse_click):
                subprocess.run(["python", "settings.py"])
            elif self.first_imp_button.clicked(mouse_click):
                return "first imp"
            elif self.second_imp_button.clicked(mouse_click):
                return "second imp"
            elif self.third_imp_button.clicked(mouse_click):
                return "third imp"


if __name__ == "__main__":
    """Para evitar que o código seja corrido automaticamente caso este módulo seja
    importado, define-se que este só será corrido caso o módulo seja corrido 
    diretamente.
    """

    menu = Menu()
    menu.get_button_press()