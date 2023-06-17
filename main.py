# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from menu import *
import subprocess

def main():
    """Corre o programa.
    
    Cria um menu e espera que o utilizador pressione um botão. Em seguida, 
    verifica se o botão pressionado foi o de sair - nesse caso, quebra o loop e 
    encerra o programa. Caso, pelo contrário, o utilizador tenha escolhido uma 
    das implementações, corre-a como subprocess. Quando o subprocess é encerrado,
    retorna ao menu.
    """
    while True:
        """O loop garante que, até o utilizador pressionar o botão de encerramento,
        depois de cada implementação o menu é aberto novamente e a ordem do 
        utilizador é recolhida.
        """

        menu = Menu()
        user_order = menu.get_button_press()
        menu.win.close()
        if user_order == "quit":
            break
        elif user_order == "first imp":
            subprocess.run(["python", "first_implementation.py"])
        elif user_order == "second imp":
            subprocess.run(["python", "second_implementation.py"])
        elif user_order == "third imp":
            subprocess.run(["python", "third_implementation.py"])

if __name__ == "__main__":
    """Para evitar que o código seja corrido automaticamente caso este módulo seja
    importado, define-se que este só será corrido caso o módulo seja corrido
    diretamente.
    """

    main()
    exit()





