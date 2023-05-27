import graphics

class Obstacle:
    def __init__(self, coords):
        self.coords = coords

    def draw(self, win):
        self.draw(win)

    def check_collision(self):
        pass

    def check_interception(self):
        pass


class Table(Obstacle):
    def __init__(self, coords):
        self.shape = "circle"
        super().__init__(coords)
        pass

class Chair(Obstacle):
    def __init__(self, coords):
        self.shape = "square"
        super().__init__(coords)
        pass


