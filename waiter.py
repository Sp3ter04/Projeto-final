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
        self.grid = initialize_algorithm(self.cell_width, obstacle_list, self.win)

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
    
    def move(self, target):
        dx, dy = self.get_vector(target)
        while self.continue_moving(target):
            self.body.move(dx, dy)
            update(self.speed)

    def get_vector(self, target):
        delta_x, delta_y, distance = get_distance(
            target, self.body.getCenter())
        dx = delta_x / (distance * 2)
        dy = delta_y / (distance * 2)
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
        for path in station_paths.values():
            path_sizes.append(len(path))
        shortest_index = path_sizes.index(min(path_sizes))
        for point in list(station_paths.values())[shortest_index]:
            self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))

    def collision(self, obstacle_list):
        obstacle_collisions = []
        for obstacle in obstacle_list:
            obs = (obstacle.anchor.getX(), obstacle.anchor.getY())
            waiter = (self.body.getCenter().getX(), self.body.getCenter().getY())
            if obstacle.shape == "square":
                if circle_square_interception(obs, obstacle.width, waiter, self.radius):
                    obstacle_collisions.append(obstacle)
            elif obstacle.shape == "circle":
                if circle_circle_interception(obs, obstacle.radius, waiter, self.radius):
                    obstacle_collisions.append(obstacle)
        if len(obstacle_collisions) != 0:
            latest_collision = obstacle_collisions[len(obstacle_collisions) - 1]
            return True
        else:
            return False




class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed, obstacle_list, win):
        super().__init__(color, radius, anchor, tolerance, speed, obstacle_list, win)


        
    def clean_dirty_spots(self, dirty_spots):
        for spot in dirty_spots:
            spot_center = spot.body.getCenter()
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(),
                                self.body.getCenter().getY()), (spot_center.getX(), spot_center.getY()))
            for point in path:
                self.move(Point(point.x_coord + self.radius /
                                4, point.y_coord + self.radius / 4))
            self.move(spot.body.getCenter())
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

    def avoid_obstacle_horizontal(self):
        self.win.getMouse()

    def avoid_obstacle_vertical(self):
        self.win.getMouse()

    def sweep_whole_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()
            turning_x = []
            x_turned = []
            y_turn = 0.5
            for x in range(100 // (2 * self.radius)):
                turning_x.append(((x * 2 + 1) * self.radius, y_turn))
                y_turn *= -1
            print(turning_x)
            if not self.quit:
                while len(turning_x) > 0:
                    while self.body.getCenter().getX() < turning_x[0][0]:
                        if not self.collision(obstacle_list):
                            self.body.move(0.5, 0)
                        else:
                            self.avoid_obstacle_horizontal()
                        update(self.speed)
                    #self.win.getMouse()
                    self.body.move(0, turning_x[0][1])
                    while self.radius < self.body.getCenter().getY() < 100 - self.radius:
                        if not self.collision(obstacle_list):
                            self.body.move(0, turning_x[0][1])
                        else:
                            self.avoid_obstacle_vertical()
                        update(self.speed)
                    x_turned.append(turning_x[0][0])
                    turning_x.pop(0)
                    print(turning_x)
                    print(x_turned)
                
                    # self.clean_dirty_spots(dirty_spots)
                    # self.move_to_docking(docking_stations)
                    # self.start = False
            else:
                break
            self.move_to_docking(docking_stations)
            self.win.getMouse()

