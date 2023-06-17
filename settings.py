# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from button import *


def access_settings(filename):
    """Acede ao ficheiro (parâmetro filename) e devolve as definições.
    
    Cria uma lista settings, na qual vão ser armazenadas as preferências obtidas
    do ficheiro.
    Em seguida, abre o ficheiro em modo de leitura e percorre-o linha a linha, 
    selecionando apenas a informação relevante e armazenando-a na lista settings.
    Caso haja um erro na abertura do ficheiro, explicita qual o erro e informa o
    utilizador que não foi possível aceder às definições.
    Devolve a lista settings
    
    """
    settings = []
    try:
        with open(filename, "r") as file: #abre o ficheiro em modo de leitura
            for line in file:
                setting = line[line.find(":") + 1:].strip() #Para cada linha, seleciona apenas a informação contida depois dos ':' e retira-lhe os espaços
                settings.append(setting)
    except Exception as e:
        print(e)
        print("Unable to access settings")
    finally:
        return settings
    

def get_settings(filename="settings.txt"):
    """Define as preferências do utilizador, consultando o ficheiro.
    
    Por defeito, assume que o ficheiro a consultar é o 'settings.txt'. Começa por
    ler o ficheiro e criar a lista settings. Posteriormente, define os parâmetros
    do programa com base nas preferências do utilizador (utilizando os types 
    adequados para cada uma) e devolve todos os parâmetros.
    """
    
    settings = access_settings(filename) #lê as definições do ficheiro e atribui-as à lista settings
    table_radius = int(settings[0])
    chair_side = int(settings[1])
    waiter_radius = int(settings[2])
    waiter_speed = int(settings[3])
    show_grid = bool(settings[4])
    show_cleaned = bool(settings[5])
    docking_radius = waiter_radius * 1.2
    tolerance = 0.5
    return table_radius, chair_side, waiter_radius, waiter_speed, show_grid, \
        show_cleaned, docking_radius, tolerance


class SettingsMenu:
    """Cria o menu das definições.
    
    O menu inclui botão de saída; botão para guardar as alterações; botão de 
    reposição das definições originais e botões para alterar os valores de todos
    os parâmetros.
    """
    
    def __init__(self):
        """Gera o menu das definições.
        
        Começa por criar a janela do menu, recolhendo em seguida as definições 
        atualmente em vigor. Posteriormente, decora a janela e cria todos os 
        botões necessários ao funcionamento do menu.
        """
        
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
        """Decora a janela com carpete e uma área para os botões."""
        self.carpet = Rectangle(Point(4, 4),
                                Point(100 - 4, 100 - 4))
        self.carpet.setFill(color_rgb(217, 202, 165))
        self.button_container = Rectangle(Point(8, 2.5), Point(92, 97.5))
        self.button_container.setFill(color_rgb(184, 162, 125))
        self.decorations = [self.carpet, self.button_container]

    def get_text(self):
        """Cria todo o texto visível na janela.
        
        Começa por criar o título, passando, em seguida, à criação do texto
        relativo a cada um dos parâmetros - o texto dos parâmetros tem um formato
        standadrizado.
        No fim, exibe os valores atuais para todos os parâmetros
        """
        
        self.title = Text(Point(50, 85), "Definições")
        self.title.setFace("times roman")
        self.title.setStyle("bold")
        self.title.setSize(30)
        self.title.setTextColor(color_rgb(65, 66, 69))
        self.text = [self.title]
        self.get_parameters() #cria o conjunto com o texto relativo a todos os parâmetros
        for parameter in self.parameter_text: #define as condições standardizadas para todo o texto dos parâmetros
            parameter.setFace("times roman")
            parameter.setStyle("bold")
            parameter.setSize(18)
            parameter.setTextColor(color_rgb(65, 66, 69))
            self.text.append(parameter)
        self.display_parameters() #exibe os valores atuais dos parâmetros

    def get_parameters(self):
        """Cria o texto relativo a cada parâmetro.
        
        Cria e posiciona o texto de todos os indicadores dos parâmetros e 
        adiciona-o à lista de parâmetros.
        """
        
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
        self.parameter_text = [self.table_radius_txt, self.chair_side_txt,
                           self.robot_radius_txt, self.robot_speed_txt, 
                           self.show_grid_txt, self.show_cleaned_txt]

    def display_parameters(self):
        """Cria os mostradores dos valores atuais dos parâmetros.
        
        Itera a lista de parâmetros e cria um mostrador para cada um, com uma 
        localização fixa em relação à descrição de texto correspondente.
        """
        
        count = 0 #cria um contador, utilizado para iteração na lista parameter_text
        for parameter in self.parameter_text:
            display_y = parameter.getAnchor().getY() - 5 #define a posição do mostrador, em relação à posição do parameter_text correspondente
            parameter_display = Text(Point(50, display_y), f"{self.current_settings[count]}") #cria o mostrador na localização definida
            self.text.append(parameter_display)
            count += 1

    def get_buttons(self):
        """Cria os botões do menu.
        
        Começa pro criar os menus para sair, guardar e repôr as definições de 
        origem, criando posteriormente os botões de ajuste de cada um dos 
        parâmetros.
        """
        
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
        """Coordena a criação dos botões necessários para ajustar cada um dos parâmetros."""
        self.get_side_buttons(self.table_radius_txt)
        self.get_side_buttons(self.chair_side_txt)
        self.get_side_buttons(self.robot_radius_txt)
        self.get_side_buttons(self.robot_speed_txt)
        self.get_side_buttons(self.show_grid_txt, 1) #o valor 1, no fim, informa o gerador de botões que este parâmetro apenas necessita de um botão de ajuste
        self.get_side_buttons(self.show_cleaned_txt, 1)

    def get_side_buttons(self, txt, number=2):
        """Cria os botões de ajuste para cada parâmetro.
        
        Assume, por defeito, que o parâmetro requer dois botões de ajuste.
        Começa por definir a posição y que os botões terão y_min é o y do point1 
        e y_max corresponde ao do point2. Essa posição é fixa em relação ao txt 
        (texto indicativo do parâmetro) correspondente.
        Posteriormente, em função do número de botões requerido pelo parâmetro,
        passa à criação dos botões - sendo dois, um terá um '+' e outro um '-'. 
        Caso apenas um botão seja necessário, esse terá o texto 'Alterar'.
        """
        
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
        """Altera o valor do parâmetro.
        
        Quando um dos botões correspondentes é pressionado, esta função avalia o
        tipo de alteração requerida pelo utilizador e altera o parâmetro em 
        concordância. No fim, altera o valor do mostrador, para refletir a mudança
        de valor do parâmetro.
        """
        if change == "add":
            self.current_settings[value] += 1
        elif change == "subtract":
            self.current_settings[value] -= 1
        else:  # Assume que, se o tipo de mudança de valor não for especificado, se trata de uma mudança de valor de um boolean e altera o parâmetro em concordância
            if self.current_settings[value] == True:
                self.current_settings[value] = not True
                self.text[value + 7].setText("False") #Caso não se especifique que o valor exibido deve ser a string 'True' ou 'False', ao alterar o valor do parâmetro o mostrador indicará 1 ou 0
            else:
                self.current_settings[value] = True
                self.text[value + 7].setText("True")
        if change != "bool": #Exceptuando o caso dos booleans a mudança de valor do mostrador corresponde diretamente à mudança de valor do parâmetro
            self.text[value + 7].setText(self.current_settings[value])

    def check_side_buttons(self, mouse_click):
        """Verifica se o clique do utilizador foi nalgum dos botões dos parâmetros.
        
        Caso não tenha sido pressionado o botão de sair, guardar ou alterar, 
        verifica se foi pressionado algum dos botões de alteração de valores dos
        parâmetros. Caso tenha sido, altera o parâmetro correspondente em 
        concordância.
        """
        
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
        """Repõe as definições de origem.
        
        Caso seja pressionado o botão de 'repôr', altera os valores das 
        'current_settings' para aqueles contidos no ficheiro 'settings_default.txt'.
        No fim, altera os valores dos mostradores para refletir a reposição dos 
        valores originais.
        """
        
        self.current_settings = list(get_settings("settings_default.txt"))
        count = 0
        for value in self.text[7:]:
            value.setText(self.current_settings[count])
            count += 1

    def update_settings(self):
        """Atualiza o ficheiro 'settings.txt'.
        
        Caso seja pressionado o botão 'guardar', cria uma lista contendo as linhas
        do ficheiro com os valores atualizador. Em seguida, substitui oa informação
        contida no ficheiro pela versão atualizada da mesma informação (abrindo 
        o ficheiro em modo 'write'). Caso haja um erro na abertura do ficheiro,
        exbe o erro e informa o utilizador que não foi possível aceder às 
        definições.
        """
        
        settings_list = [f"TABLE_RADIUS : {self.current_settings[0]}\n", 
                     f"TABLE_SIDE : {self.current_settings[1]}\n",
                      f"ROBOT_RADIUS : {self.current_settings[2]}\n",
                       f"ROBOT_SPEED : {self.current_settings[3]}\n",
                         f"SHOW_GRID : {self.current_settings[4]}\n" if self.current_settings[4] == 1 else "SHOW_GRID : \n",
                         f"SHOW_CLEANED : {self.current_settings[5]}\n" if self.current_settings[5] == 1 else "SHOW_CLEANED : \n"] #cria a lista das linhas alteradas do ficheiro
        try:
            with open("settings.txt", "w") as file: #abre o ficheiro em modo de escrita
                for line in settings_list: #itera a lista das linhas e substitui a linha correspondente no ficheiro pela sua versão atualizada
                    file.write(line)
        except Exception as e: #Informa o utilizador que ocorreu um erro a abrir as definições
            print(e)
            print("Unable to access settings")

    def get_button_press(self):
        """Recolhe um clique do utilizador e reage em função do botão pressionado.
        
        Corre um loop para evitar erros caso o clique do utilizador não se 
        encontre dentro de nenhum dos botões.
        Se o utilizador pressionar o botão de saída, o loop é quebrado.
        Caso contrário, identifica em qual dos botões o clique se localizou e 
        reage de acordo com essa informação.
        """
        
        while True:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                self.win.close()
                break
            elif self.save_button.clicked(mouse_click):
                self.win.close()
                self.update_settings()
                break
            elif self.default_button.clicked(mouse_click):
                self.back_to_default()
            else:
                self.check_side_buttons(mouse_click)


if __name__ == "__main__":
    """Cria a janela do menu de definições e recolhe o clique do utilizador.
    
    Evita que o menu seja criado automaticamente quando o módulo é importado.
    """
    
    menu = SettingsMenu()
    menu.get_button_press()