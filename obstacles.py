from graphics import *

#TABLE_RADIUS
#CHAIR_SIDE
obstacle_list = []

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
    def __init__(self, color, anchor, side):
        super().__init__(color, anchor)
        self.side = side
        self.shape = "square"
        self.p1 = Point(anchor[0] - self.side / 2, anchor[1] - self.side / 2)
        self.p2 = Point(anchor[0] + self.side / 2, anchor[1] + self.side / 2)
        self.body = Rectangle(self.p1, self.p2)
        self.body.setFill(self.color)
