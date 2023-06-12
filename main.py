from first_implementation import *
from second_implementation import *
from third_implementation import *
from menu import *

def main():
    while True:
        menu = Menu()
        user_order = menu.get_button_press()
        menu.win.close()
        if user_order == "quit":
            break
        elif user_order == "first imp":
            first_implementation()
        elif user_order == "second imp":
            second_implementation()
        elif user_order == "third imp":
            third_implementation()


main()
exit()





