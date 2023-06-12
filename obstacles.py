from graphics import *
from random import randint

obstacle_list = []
docking_stations = []

class Obstacle:
    def __init__(self, anchor):
        self.anchor = Point(anchor[0], anchor[1])
        obstacle_list.append(self)

    def draw(self, win):
        for entity in self.body_entities:
            entity.draw(win)

    def check_collision(self):
        pass

    def check_interception(self):
        pass


class Table(Obstacle):
    def __init__(self, anchor, radius):
        super().__init__(anchor)
        self.radius = radius
        self.shape = "circle"
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(82, 96, 112))
        self.body_entities = [self.body]
        self.get_towel(self.radius * 0.72, "white")
        self.get_towel(self.radius * 0.67, color_rgb(82, 96, 112))
        self.get_towel(self.radius * 0.50, color_rgb(254, 220, 86))
        self.get_towel(self.radius * 0.45, color_rgb(82, 96, 112))
        self.get_dishes()

    def get_dishes(self):
        dish_radius = self.radius * 0.3
        dishes = []
        point1 = Point(self.anchor.getX() + self.radius * 0.65, self.anchor.getY())
        point2 = Point(self.anchor.getX() - self.radius * 0.65, self.anchor.getY())
        point3 = Point(self.anchor.getX(), self.anchor.getY() + self.radius * 0.65)
        point4 = Point(self.anchor.getX(), self.anchor.getY() - self.radius * 0.65)
        for point in [point1, point2, point3, point4]:
            dishes.append(self.get_dish(point, dish_radius))
        for dish in dishes:
            for entity in dish:
                self.body_entities.append(entity)
        

    def get_dish(self, anchor, radius):
        outer_circle = Circle(anchor, radius)
        outer_circle.setFill("white")
        inner_circle = Circle(anchor, radius * 0.75)
        inner_circle.setFill(color_rgb(250, 249, 254))
        dish = [outer_circle, inner_circle]
        return dish

    def get_towel(self, radius, color):
        towel = Circle(self.anchor, radius)
        towel.setFill(color)
        self.body_entities.append(towel)

class Chair(Obstacle):
    def __init__(self, anchor, width):
        super().__init__(anchor)
        self.width = width
        self.shape = "square"
        self.p2 = Point(anchor[0] + self.width, anchor[1] + self.width)
        self.hole = self.get_hole()
        self.body = Rectangle(self.anchor, self.p2)
        self.body.setFill(color_rgb(184, 162, 125))
        self.body_entities = [self.body, self.hole]

    def get_hole(self):
        center = Point(self.anchor.getX() + self.width / 2, self.anchor.getY() + self.width / 2)
        hole = Circle(center, self.width * 0.15)
        hole.setFill(color_rgb(217, 202, 165))
        return hole

class Docking:
    def __init__(self, anchor, radius):
        docking_stations.append(self)
        self.anchor = Point(anchor[0], anchor[1])
        self.shape = "circle"
        self.radius = radius
        self.box = self.get_box()
        self.inner_circle = Circle(self.anchor, radius * 0.92)
        self.inner_circle.setFill(color_rgb(65, 66, 69))
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(82, 96, 112))
        self.body_entities = [self.box, self.body, self.inner_circle]

    def get_box(self):
        point1 = Point(self.anchor.getX() - self.radius, self.anchor.getY() - self.radius)
        point2 = Point(self.anchor.getX() + self.radius,self.anchor.getY() + self.radius)
        box = Rectangle(point1, point2)
        box.setFill(color_rgb(41, 39, 39))
        return box

    def draw(self, win):
        for entity in self.body_entities:
            entity.draw(win)

class Dirt:
    def __init__(self, anchor, waiter, win):
        self.anchor = anchor
        self.radius = waiter.radius * 1.2
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(250, 249, 254))
        self.body_entities = [self.body]
        self.get_yolk()
        self.draw(win)
        self.shape = "circle"
        waiter.undraw()
        waiter.draw()
        # for entity in waiter.body_entities:
        #     entity.undraw()
        #     entity.draw(win)

    def get_yolk(self):
        yolk_y_positions = [-0.18 * self.radius, 0, 0.18 * self.radius]
        yolk_x_positions = [-0.18 * self.radius, 0.18 * self.radius]
        center = Point(self.anchor.getX() + yolk_x_positions[randint(0, 1)], self.anchor.getY() + yolk_y_positions[randint(0, 2)])
        yolk = Circle(center, self.radius * 0.4)
        yolk.setFill(color_rgb(250, 129, 36))
        self.body_entities.append(yolk)

    def draw(self, win):
        for entity in self.body_entities:
            entity.draw(win)

    def cleaned(self):
        for entity in self.body_entities:
            entity.undraw()



def teste():
    win = GraphWin("test window", 500, 500)
    chair1 = Chair("black", (250, 250), 10)
    chair1.draw(win)
    win.getMouse()

if __name__ == "__main__":
    teste()