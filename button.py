# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *

class Button:
    """Cria um botão.

    As dimensões, cores e texto são definidas para cada botão.
    """

    def __init__(self, point1, point2, outer_color, inner_color, text, text_color, text_size):
        """Gera o botão.
        
        Toma como parâmetros os pontos dos cantos opostos do botão (point1 e 
        point2); a cor da zona externa do botão; cor da zona interior; texto que 
        deve ser exibido no botão, com a respetiva cor e tamanho.
        """

        self.point1 = point1
        self.point2 = point2
        self.entities = []
        text_anchor = Point((point1.getX() + point2.getX()) / 2, (point1.getY() + point2.getY()) / 2)
        self.get_body(inner_color, outer_color)
        self.get_text(text_anchor, text, text_color, text_size)

    def get_body(self, inner_color, outer_color):
        """Cria a caixa do botão.
        
        O botão é quadrado e tem um outline de 5px, por defeito.
        """

        self.body = Rectangle(self.point1, self.point2)
        self.body.setFill(inner_color)
        self.body.setWidth(5)
        self.body.setOutline(outer_color)
        self.entities.append(self.body)

    def get_text(self, text_anchor, text, text_color, text_size):
        """Formata o texto do interior do botão."""
        self.text = Text(text_anchor, text)
        self.text.setTextColor(text_color)
        self.text.setSize(text_size)
        self.text.setStyle("bold")
        self.text.setFace("times roman")
        self.entities.append(self.text)

    def draw(self, win):
        """Desenha na janela todas as entidades que constituem o botão."""
        for entity in self.entities:
            entity.draw(win)

    def undraw(self):
        """Retira da janela todas as entidades que constituem o botão."""
        for entity in self.entities:
            entity.undraw()

    def clicked(self, mouse_click):
        """Define se o utilizador clicou no botão.
        
        Verifica se o mouse_click se encontra dentro dos limites do botão
        e retorna True se este tiver sido pressionado. Caso contrário, retorna
        False.
        """
        
        if self.point1.getX() < mouse_click.getX() < self.point2.getX() and \
                self.point1.getY() < mouse_click.getY() < self.point2.getY():
            return True
        return False
