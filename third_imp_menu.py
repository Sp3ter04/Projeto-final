from button import *
from graphics import *

class third_imp_menu:
    def __init__(self, first_button_text, second_button_text, first_button_return, second_button_return):
        self.first_button_text = first_button_text
        self.second_button_text = second_button_text
        self.first_button_return = first_button_return
        self.second_button_return = second_button_return
        self.win = GraphWin("Menu", 500, 500)
        self.win.setCoords(0, 0, 100, 100)
        self.win.setBackground(color_rgb(61, 36, 1))
        self.get_decorations()
        self.get_text()
        self.get_buttons()
        for decoration in self.decorations:
            decoration.draw(self.win)
        self.instructions.draw(self.win)
        for button in self.buttons:
            button.draw(self.win)

    def get_decorations(self):
        self.carpet = Rectangle(Point(4, 4),
                                Point(100 - 4, 100 - 4))
        self.carpet.setFill(color_rgb(217, 202, 165))
        self.button_container = Rectangle(Point(8, 2.5), Point(92, 97.5))
        self.button_container.setFill(color_rgb(184, 162, 125))
        self.decorations = [self.carpet, self.button_container]

    def get_text(self):
        self.instructions = Text(Point(50, 70), "Selecione o mode de funcionamento")
        self.instructions.setFace("times roman")
        self.instructions.setStyle("bold")
        self.instructions.setSize(18)
        self.instructions.setTextColor(color_rgb(65, 66, 69))

    def get_buttons(self):
        self.random_button = Button(Point(20, 50), Point(80, 60), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), self.first_button_text, color_rgb(65, 66, 69), 13)
        self.file_button = Button(Point(20, 35), Point(80, 45), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), self.second_button_text, color_rgb(65, 66, 69), 13)
        self.quit_button = Button(Point(0, 100.5 - 4), Point(
            4, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", color_rgb(41, 39, 39), 13)
        self.quit_button.body.setWidth(1)
        self.buttons = [self.random_button, self.file_button, self.quit_button]

    def get_button_press(self):
        while True:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                self.win.close()
                return "quit"
            elif self.random_button.clicked(mouse_click):
                self.win.close()
                return self.first_button_return
            elif self.file_button.clicked(mouse_click):
                self.win.close()
                return self.second_button_return
