from graphics import *
from obstacles import *
from waiter import *
import time
from math import sqrt

WAITER_COLOR = "blue"
WAITER_RADIUS = 2.5
WAITER_ANCHOR = (50, 50)
WAITER_SPEED = 100

TOLERANCE = 0.5

obstacle_list = []

def get_distance(p1, p2):
    delta_x = p1.getX() - p2.getX()
    delta_y = p1.getY() - p2.getY()
    distance = sqrt(delta_x**2 + delta_y**2)
    return delta_x, delta_y, distance

class Waiter:
    def __init__(self, color, radius, anchor):
        self.color = color
        self.radius = radius
        self.anchor = Point(anchor[0], anchor[1])
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(self.color)

    def draw(self, win):
        self.body.draw(win)

    def get_vector(self, target):
        delta_x, delta_y, distance = get_distance(target, self.body.getCenter())
        dx = delta_x / distance
        dy = delta_y / distance
        return dx, dy
    
    def continue_moving(self, target):
        distance = get_distance(target, self.body.getCenter())[2]
        if not int(distance*10) in range(int(TOLERANCE*10)):
            return True
        else:
            return False

    def move(self, target):
        dx, dy = self.get_vector(target)
        while self.continue_moving(target):
            self.body.move(dx, dy)
            update(WAITER_SPEED)
        pass
        


    def spin(self):
        pass

    def back_to_docking(self):
        pass


class Waiter1(Waiter):
    def __init__(self, color, radius, anchor):
        super().__init__(color, radius, anchor)

    def clean_room(self):
        pass


class Waiter2(Waiter):
    def __init__(self, color, radius, anchor):
        super().__init__(color, radius, anchor)

    def sweep_whole_room(self):
        pass


class Waiter3(Waiter):
    def __init__(self, color, radius, anchor):
        super().__init__(color, radius, anchor)

    def clean_room(self):
        pass


class Obstacle:
    def __init__(self, anchor):
        self.coords = anchor
        obstacle_list.append(self)

    def draw(self, win):
        self.draw(win)

    def check_collision(self):
        pass

    def check_interception(self):
        pass


class Table(Obstacle):
    def __init__(self, anchor):
        super().__init__(anchor)
        self.shape = "circle"
        pass


class Chair(Obstacle):
    def __init__(self, anchor):
        super().__init__(anchor)
        self.shape = "square"
        pass




def main():
    win = GraphWin("Trial version", 800, 800)
    win.setCoords(0, 0, 100, 100)
    win.setBackground("white")
    waiter = Waiter1(WAITER_COLOR, WAITER_RADIUS, WAITER_ANCHOR)
    waiter.draw(win)
    waiter.move(win.getMouse())
    win.getMouse()
    win.close()

main()






