from graphics import *
from universal_functions import *
from obstacles import *
from button import Button

TABLE_RADIUS = 12
CHAIR_SIDE = 6
WAITER_RADIUS = 4
WAITER_SPEED = 120
DOCKING_RADIUS = WAITER_RADIUS * 1.2
TOLERANCE = 0.5


class Menu:
    def __init__(self):
        self.win = GraphWin("Trial version", 800, 800)
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
        self.carpet = Rectangle(Point(WAITER_RADIUS, WAITER_RADIUS),
                        Point(100 - WAITER_RADIUS, 100 - WAITER_RADIUS))
        self.carpet.setFill(color_rgb(217, 202, 165))
        self.docking1 = Docking((DOCKING_RADIUS, DOCKING_RADIUS), DOCKING_RADIUS)
        self.docking2 = Docking((100 - DOCKING_RADIUS, 100 -
                        DOCKING_RADIUS), DOCKING_RADIUS)
        self.button_container = Rectangle(Point(8, 2.5), Point(92, 97.5))
        self.button_container.setFill(color_rgb(184, 162, 125))
        self.decorations = [self.carpet, self.docking1, self.docking2, self.button_container]

    def get_text(self):
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
        self.first_imp_button = Button(Point(20, 50), Point(80, 60), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Primeira Implementação", color_rgb(65, 66, 69), 13)
        self.second_imp_button = Button(Point(20, 35), Point(80, 45), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Segunda Implementação", color_rgb(65, 66, 69), 13)
        self.third_imp_button = Button(Point(20, 20), Point(80, 30), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Terceira Implementação", color_rgb(65, 66, 69), 13)
        self.quit_button = Button(Point(0, 100.5 - WAITER_RADIUS), Point(
            WAITER_RADIUS, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", color_rgb(41, 39, 39), 13)
        self.quit_button.body.setWidth(1)
        self.buttons = [self.quit_button, self.first_imp_button, self.second_imp_button, self.third_imp_button]

    def get_button_press(self):
        while True:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                return "quit"
            elif self.first_imp_button.clicked(mouse_click):
                return "first imp"
            elif self.second_imp_button.clicked(mouse_click):
                return "second imp"
            elif self.third_imp_button.clicked(mouse_click):
                return "third imp"


if __name__ == "__main__":
    menu = Menu()
    menu.win.getMouse()