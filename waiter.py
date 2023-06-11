from graphics import *
from math import cos, sin
from shortest_path import *
from universal_functions import *
from obstacles import *


class Waiter:
    def __init__(self, color, radius, anchor, tolerance, speed, obstacle_list, win):
        self.body_entities = []
        self.win = win
        self.color = color
        self.radius = radius
        self.anchor = Point(anchor[0], anchor[1])
        self.tolerance = tolerance
        self.speed = speed
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(self.color)
        self.quit = False
        self.start = False
        self.cell_width = self.radius / 2

    def draw(self):
        self.body.draw(self.win)

    def get_dirty_spots(self):
        dirty_spots = []
        while not self.start:
            mouse_click = self.win.getMouse()
            if mouse_click.getX() >= 90 and mouse_click.getY() <= 10:
                    self.quit = True
                    break
            if mouse_click.getX() <= 10 and mouse_click.getY() >= 90:
                self.start = True
            else:
                path_to_dirt = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(),
                                            self.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()))
                if path_to_dirt == None:
                    error_message = Text(
                        Point(50, 94), "Target Cannot be Reached")
                    error_message.draw(self.win)
                    time.sleep(0.8)
                    error_message.undraw()
                    continue

                dirt = Dirt(mouse_click, self, self.win)
                dirty_spots.append(dirt)

        return dirty_spots
    
    def move_with_shortest_path(self, target, dirty_spots=[]):
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(),
                self.body.getCenter().getY()), (target.getX(), target.getY()))
            for point in path:
                if len(dirty_spots) > 0:
                    if self.collision(dirty_spots):
                        return_spot = self.body.getCenter()
                        spot = self.latest_collision
                        self.move(spot.body.getCenter())
                        self.clean_spot()
                        dirty_spots.remove(spot)
                        spot.cleaned()
                        self.move(return_spot)
                self.move(Point(point.x_coord + self.radius /
                                4, point.y_coord + self.radius / 4))
            self.move(target)
    
    def move(self, target):
        dx, dy = self.get_vector(target)
        while self.continue_moving(target):
            self.body.move(dx, dy)
            update(self.speed)

    def get_vector(self, target):
        delta_x, delta_y, distance = get_distance(
            target, self.body.getCenter())
        dx = delta_x / (distance * 2 + 0.01)
        dy = delta_y / (distance * 2 + 0.01)
        return dx, dy

    def continue_moving(self, target):
        distance = get_distance(target, self.body.getCenter())[2]
        if not int(distance*10) in range(int(self.tolerance*10)):
            return True
        else:
            return False

    def clean_spot(self):
        dirt_center = self.body.getCenter()
        theta = 0
        spiral = 0
        while spiral < 0.4 * self.radius:
            x = dirt_center.getX() + spiral * cos(theta)
            y = dirt_center.getY() + spiral * sin(theta)

            dx = x - self.body.getCenter().getX()
            dy = y - self.body.getCenter().getY()

            self.body.move(dx, dy)

            theta += 0.30
            spiral += 0.02

            update(self.speed / 2)
        

    def move_to_docking(self, docking_stations):
        station_paths = {}
        path_sizes = []
        for station in docking_stations:
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(), 
                                self.body.getCenter().getY()), (station.anchor.getX(), station.anchor.getY()))
            station_paths.update({station : path})
        try:
            for path in station_paths.values():
                path_sizes.append(len(path))
        except:
            pass
        shortest_index = path_sizes.index(min(path_sizes))
        for point in list(station_paths.values())[shortest_index]:
            self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))
        self.move(docking_stations[shortest_index].anchor)

    def collision(self, entity_list, tolerance=0):
        collisions = []
        for entity in entity_list:
            ent = (entity.anchor.getX(), entity.anchor.getY())
            waiter = (self.body.getCenter().getX(), self.body.getCenter().getY())
            if entity.shape == "square":
                if circle_square_interception(ent, entity.width, waiter, self.radius, tolerance):
                    collisions.append(entity)
            elif entity.shape == "circle":
                if circle_circle_interception(ent, entity.radius, waiter, self.radius, tolerance):
                    collisions.append(entity)
        if len(collisions) != 0:
            self.latest_collision = collisions[len(collisions) - 1]
            return True
        else:
            return False




class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed, obstacle_list, win):
        super().__init__(color, radius, anchor, tolerance, speed, obstacle_list, win)
        self.grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 3, self.cell_width * 1.7, self.cell_width * 2)[0]


        
    def clean_dirty_spots(self, dirty_spots):
        for spot in dirty_spots:
            spot_center = spot.body.getCenter()
            self.move_with_shortest_path(spot_center)
            self.clean_spot()
            spot.cleaned()



    def clean_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()            
            if not self.quit:
                self.clean_dirty_spots(dirty_spots)
                self.move_to_docking(docking_stations)
                self.start = False
            else:
                break



class Waiter23(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed, obstacle_list, win):
        super().__init__(color, radius, anchor, tolerance, speed, obstacle_list, win)
        self.grid, self.non_obstacle_grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 2, self.cell_width * 2)
        self.latest_collision = None

    def clean_whole_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()
            for row in self.non_obstacle_grid:
                for spot in row:
                    spot.clean = False
            for row in self.non_obstacle_grid[3::4]:
                for spot in row:
                    for neighbor in spot.neighbors:
                        for second_neighbor in neighbor.neighbors:
                            if self.collision([second_neighbor]):
                                second_neighbor.clean = True
                                #second_neighbor.get_square(self.win, "blue")
                    if not spot.clean:
                        spot_anchor = (spot.anchor.getX(), spot.anchor.getY())
                        target = Point(
                            spot_anchor[0] + self.cell_width/2, spot_anchor[1] + self.cell_width/2)
                        self.move_with_shortest_path(target, dirty_spots)
            self.move_to_docking(docking_stations)
            self.start = False

