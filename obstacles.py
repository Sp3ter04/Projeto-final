from graphics import *
# from waiter import *

#TABLE_RADIUS
#CHAIR_SIDE
obstacle_list = []
docking_stations = []

class Obstacle:
    def __init__(self, color, anchor):
        self.anchor = Point(anchor[0], anchor[1])
        obstacle_list.append(self)
        self.color = color

    def draw(self, win):
        self.body.draw(win)

    def check_collision(self):
        pass

    def check_interception(self):
        pass


class Table(Obstacle):
    def __init__(self, color, anchor, radius):
        super().__init__(color, anchor)
        self.radius = radius
        self.shape = "circle"
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(self.color)


class Chair(Obstacle):
    def __init__(self, color, anchor, width):
        super().__init__(color, anchor)
        self.width = width
        self.shape = "square"
        self.p2 = Point(anchor[0] + self.width, anchor[1] + self.width)
        self.body = Rectangle(self.anchor, self.p2)
        self.body.setFill(self.color)

class Docking:
    def __init__(self, anchor):
        docking_stations.append(self)
        self.anchor = Point(anchor[0], anchor[1])
        self.body = Circle(self.anchor, 5)
        self.body.setFill("orange")

    def draw(self, win):
        self.body.draw(win)

class Dirt:
    def __init__(self, anchor, waiter, win):
        self.anchor = anchor
        self.body= Circle(self.anchor, waiter.radius * 1.2)
        self.body.setFill("black")
        self.body.draw(win)
        waiter.body.undraw()
        waiter.body.draw(win)#waiter_center, win)

    def draw(self, win):
        self.body.draw(win)

    def cleaned(self):
        self.body.undraw()



def teste():
    win = GraphWin("test window", 500, 500)
    chair1 = Chair("black", (250, 250), 10)
    chair1.draw(win)
    win.getMouse()

if __name__ == "__main__":
    teste()