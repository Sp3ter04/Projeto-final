from graphics import *

class Waiter:
    def __init__(self, color, radius, anchor):
        self.color = color
        self.radius = radius
        self.anchor = Point(anchor[0], anchor[1])
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(self.color)

    def draw(self, win):
        self.body.draw(win)

    def move(self, dx, dy):
        self.anchor._move(dx, dy)

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
    def __init__(self, color, radius):
        super().__init__(color, radius)

    def sweep_whole_room(self):
        pass

class Waiter3(Waiter):
    def __init__(self, color, radius):
        super().__init__(color, radius)

    def clean_room(self):
        pass

