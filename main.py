# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from menu import *
import subprocess

def main():
    while True:
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


main()
exit()





