from graphics import *
from button import *


def access_settings(filename):
    settings = []
    try:
        with open(filename, "r") as file:
            for line in file:
                setting = line[line.find(":") + 1:].strip()
                settings.append(setting)
    except Exception as e:
        print(e)
        print("Unable to access settings")
    finally:
        return settings
    

def get_settings(filename="settings.txt"):
    settings = access_settings(filename)
    table_radius = int(settings[0])
    chair_side = int(settings[1])
    waiter_radius = int(settings[2])
    waiter_speed = int(settings[3])
    show_grid = bool(settings[4])
    show_cleaned = bool(settings[5])
    docking_radius = waiter_radius * 1.2
    tolerance = 0.5
    return table_radius, chair_side, waiter_radius, waiter_speed, show_grid, show_cleaned, docking_radius, tolerance

def change_settigs():
    pass

class SettingsMenu:
    def __init__(self):
        self.win = GraphWin("Menu", 500, 750)
        self.win.setCoords(0, 0, 100, 100)
        self.win.setBackground(color_rgb(61, 36, 1))
        self.current_settings = list(get_settings())
        self.get_decorations()
        self.get_text()
        self.get_buttons()
        for decoration in self.decorations:
            decoration.draw(self.win)
        for text in self.text:
            text.draw(self.win)
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
        self.title = Text(Point(50, 85), "Definições")
        self.title.setFace("times roman")
        self.title.setStyle("bold")
        self.title.setSize(30)
        self.title.setTextColor(color_rgb(65, 66, 69))
        self.instructions = Text(Point(50, 70), "Selecione o mode de funcionamento")
        self.text = [self.title]
        self.get_parameters()
        for parameter in self.parameters:
            parameter.setFace("times roman")
            parameter.setStyle("bold")
            parameter.setSize(18)
            parameter.setTextColor(color_rgb(65, 66, 69))
            self.text.append(parameter)
        self.display_parameters()

    def get_parameters(self):
        self.table_radius_txt = Text(
            Point(50, 75), "Raio da Mesa")
        self.chair_side_txt = Text(
            Point(50, 65), "Lado da Cadeira")
        self.robot_radius_txt = Text(
            Point(50, 55), "Raio do Robot")
        self.robot_speed_txt = Text(
            Point(50, 45), "Velocidade do Robot")
        self.show_grid_txt = Text(
            Point(50, 35), "Mostrar a Grelha?")
        self.show_cleaned_txt = Text(
            Point(50, 25), "Mostrar a área limpa?")
        self.parameters = [self.table_radius_txt, self.chair_side_txt,
                           self.robot_radius_txt, self.robot_speed_txt, 
                           self.show_grid_txt, self.show_cleaned_txt]

    def display_parameters(self):
        count = 0
        for parameter in self.parameters:
            display_y = parameter.getAnchor().getY() - 5
            parameter_display = Text(Point(50, display_y), f"{self.current_settings[count]}")
            self.text.append(parameter_display)
            count += 1

    def get_buttons(self):
        self.quit_button = Button(Point(0, 100.5 - 4), Point(
            4, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", color_rgb(41, 39, 39), 13)
        self.quit_button.body.setWidth(1)
        self.save_button = button = Button(Point(70, 5), Point(85, 10), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Guardar", color_rgb(65, 66, 69), 13)
        self.default_button = button = Button(Point(15, 5), Point(30, 10), color_rgb(
            250, 249, 254), color_rgb(217, 202, 165), "Repôr", color_rgb(65, 66, 69), 13)
        self.buttons = [self.quit_button, self.save_button, self.default_button]
        self.get_parameter_buttons()

    def get_parameter_buttons(self):
        self.get_side_buttons(self.table_radius_txt)
        self.get_side_buttons(self.chair_side_txt)
        self.get_side_buttons(self.robot_radius_txt)
        self.get_side_buttons(self.robot_speed_txt)
        self.get_side_buttons(self.show_grid_txt, 1)
        self.get_side_buttons(self.show_cleaned_txt, 1)

    def get_side_buttons(self, txt, number=2):
        button_y_max = txt.getAnchor().getY() - 4
        button_y_min = button_y_max - 3
        if number == 2:
            button_1 = Button(Point(15, button_y_min), Point(19, button_y_max), color_rgb(
                250, 249, 254), color_rgb(217, 202, 165), "-", color_rgb(65, 66, 69), 13)
            self.buttons.append(button_1)
            button_2 = Button(Point(81, button_y_min), Point(85, button_y_max), color_rgb(
                250, 249, 254), color_rgb(217, 202, 165), "+", color_rgb(65, 66, 69), 13)
            self.buttons.append(button_2)
        else:
            button = Button(Point(70, button_y_min), Point(85, button_y_max), color_rgb(
                250, 249, 254), color_rgb(217, 202, 165), "Alterar", color_rgb(65, 66, 69), 13)
            self.buttons.append(button)

    def change_value(self, value, change="bool"):
        if change == "add":
            self.current_settings[value] += 1
        elif change == "subtract":
            self.current_settings[value] -= 1
        else:
            if self.current_settings[value] == True:
                self.current_settings[value] = not True
            else:
                self.current_settings[value] = True
        self.text[value + 7].setText(self.current_settings[value])

    def check_side_buttons(self, mouse_click):
        if self.buttons[3].clicked(mouse_click):
            self.change_value(0, "subtract")
        if self.buttons[4].clicked(mouse_click):
            self.change_value(0, "add")
        if self.buttons[5].clicked(mouse_click):
            self.change_value(1, "subtract")
        if self.buttons[6].clicked(mouse_click):
            self.change_value(1, "add")
        if self.buttons[7].clicked(mouse_click):
            self.change_value(2, "subtract")
        if self.buttons[8].clicked(mouse_click):
            self.change_value(2, "add")
        if self.buttons[9].clicked(mouse_click):
            self.change_value(3, "subtract")
        if self.buttons[10].clicked(mouse_click):
            self.change_value(3, "add")
        if self.buttons[11].clicked(mouse_click):
            self.change_value(4, "bool")
        if self.buttons[12].clicked(mouse_click):
            self.change_value(5, "bool")
        
    def back_to_default(self):
        self.current_settings = list(get_settings("settings_default.txt"))
        count = 0
        for value in self.text[7:]:
            value.setText(self.current_settings[count])
            count += 1

    def update_settings(self):
        settings_list = [f"TABLE_RADIUS : {self.current_settings[0]}\n", 
                     f"TABLE_SIDE : {self.current_settings[1]}\n",
                      f"ROBOT_RADIUS : {self.current_settings[2]}\n",
                       f"ROBOT_SPEED : {self.current_settings[3]}\n",
                        f"SHOW_GRID : {self.current_settings[4]}\n" if self.current_settings[4] == 1 else "\n",
                         f"SHOW_CLEANED : {self.current_settings[5]}\n" if self.current_settings[5] == 1 else "\n"]
        try:
            with open("settings.txt", "w") as file:
                for line in settings_list:
                    file.write(line)
        except Exception as e:
            print(e)
            print("Unable to access settings")

    def get_button_press(self):
        while True:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                self.win.close()
            elif self.save_button.clicked(mouse_click):
                self.win.close()
                self.update_settings()
            elif self.default_button.clicked(mouse_click):
                self.back_to_default()
            else:
                self.check_side_buttons(mouse_click)


if __name__ == "__main__":
    menu = SettingsMenu()
    menu.get_button_press()