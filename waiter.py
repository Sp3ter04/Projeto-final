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

    def clean_spot(self):
        pass

    def move_to_docking(self, docking_stations):
        station_paths = {}
        path_sizes = []
        for station in docking_stations:
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(
            ), self.body.getCenter().getY()), (station.anchor.getX(), station.anchor.getY()))
            station_paths.update({station : path})
        for path in station_paths.values():
            path_sizes.append(len(path))
        shortest_index = path_sizes.index(min(path_sizes))
        for point in list(station_paths.values())[shortest_index]:
            self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))


    def spin(self):
        pass




class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed):
        super().__init__(color, radius, anchor, tolerance, speed)

    def clean_room(self, obstacle_list, docking_stations, win):
        self.cell_width = self.radius / 2
        self.grid = initialize_algorithm(self.cell_width, obstacle_list, win)
        while True:
            mouse_click = win.getMouse()
            try:
                path_to_dirt = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(), 
                                    self.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()))
                for point in path_to_dirt:
                    self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))
                self.move(mouse_click)
                win.getMouse()
                self.move_to_docking(docking_stations)
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
