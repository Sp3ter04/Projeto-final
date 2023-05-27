from graphics import *
from math import sqrt

# TOLERANCE
# WAITER_SPEED


def get_distance(p1, p2):
    delta_x = p1.getX() - p2.getX()
    delta_y = p1.getY() - p2.getY()
    distance = sqrt(delta_x**2 + delta_y**2)
    return delta_x, delta_y, distance


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

    def spin(self):
        pass

    def back_to_docking(self):
        pass


class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed):
        super().__init__(color, radius, anchor, tolerance, speed)

    def clean_room(self):
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
