from graphics import *


class Button:
    def __init__(self, point1, point2, outer_color, inner_color, text, text_color, text_size):
        self.point1 = point1
        self.point2 = point2
        self.entities = []
        text_anchor = Point((point1.getX() + point2.getX()) / 2, (point1.getY() + point2.getY()) / 2)
        self.get_body(inner_color, outer_color)
        self.get_text(text_anchor, text, text_color, text_size)

    def get_body(self, inner_color, outer_color):
        self.body = Rectangle(self.point1, self.point2)
        self.body.setFill(inner_color)
        self.body.setWidth(5)
        self.body.setOutline(outer_color)
        self.entities.append(self.body)

    def get_text(self, text_anchor, text, text_color, text_size):
        self.text = Text(text_anchor, text)
        self.text.setTextColor(text_color)
        self.text.setSize(text_size)
        self.text.setStyle("bold")
        self.text.setFace("times roman")
        self.entities.append(self.text)

    def draw(self, win):
        for entity in self.entities:
            entity.draw(win)

    def undraw(self):
        for entity in self.entities:
            entity.undraw()

    def clicked(self, mouse_click):
        if self.point1.getX() < mouse_click.getX() < self.point2.getX() and \
                self.point1.getY() < mouse_click.getY() < self.point2.getY():
            return True
        return False
