from graphics import *
from math import sqrt
from shortest_path import *
from universal_functions import *


class Waiter:
    def __init__(self, color, radius, anchor, tolerance, speed):
        self.color = color
        self.radius = radius
        self.anchor = Point(anchor[0], anchor[1])
        self.tolerance = tolerance
        self.speed = speed
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(self.color)

    def draw(self, win):
        self.body.draw(win)

    def get_vector(self, target):
        delta_x, delta_y, distance = get_distance(
            target, self.body.getCenter())
        dx = delta_x / distance
        dy = delta_y / distance
        return dx, dy

    def continue_moving(self, target):
        distance = get_distance(target, self.body.getCenter())[2]
        if not int(distance*10) in range(int(self.tolerance*10)):
            return True
        else:
            return False

    def move(self, target):
        dx, dy = self.get_vector(target)
        while self.continue_moving(target):
            self.body.move(dx, dy)
            update(self.speed)
        pass

    def move_to_docking(self):
        pass

    def spin(self):
        pass




class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed):
        super().__init__(color, radius, anchor, tolerance, speed)

    def clean_room(self, obstacle_list, win):
        cell_width = self.radius / 2
        grid = initialize_algorithm(cell_width, obstacle_list, win)
        while True:
            mouse_click = win.getMouse()
            try:
                path_to_dirt = run_algorithm(cell_width, grid, (self.body.getCenter().getX(), self.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()))
                for point in path_to_dirt:
                    self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))
                self.move(mouse_click)
            except:
                error_message = Text(Point(50, 94), "Target Cannot be Reached")
                error_message.draw(win)
                time.sleep(0.8)
                error_message.undraw()
        pass


class Waiter2(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed):
        super().__init__(color, radius, anchor, tolerance, speed)

    def sweep_whole_room(self):
        pass


class Waiter3(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed):
        super().__init__(color, radius, anchor, tolerance, speed)

    def clean_room(self):
        pass
