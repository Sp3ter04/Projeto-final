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
    
    def move_with_shortest_path(self, target):
            path = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(),
                self.body.getCenter().getY()), (target.getX(), target.getY()))
            for point in path:
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
        try:
            for path in station_paths.values():
                path_sizes.append(len(path))
        except:
            pass
        shortest_index = path_sizes.index(min(path_sizes))
        for point in list(station_paths.values())[shortest_index]:
            self.move(Point(point.x_coord + self.radius / 4, point.y_coord + self.radius / 4))
        self.move(docking_stations[shortest_index].anchor)

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
            self.latest_collision = obstacle_collisions[len(obstacle_collisions) - 1]
            return obstacle_collisions
        else:
            return False




class Waiter1(Waiter):
    def __init__(self, color, radius, anchor, tolerance, speed, obstacle_list, win):
        super().__init__(color, radius, anchor, tolerance, speed, obstacle_list, win)


        
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
        self.latest_collision = None

    def path_inversion(self):
        for point in self.turning_x:
            point[1] *= -1
        self.body.move(0, self.turning_x[0][1])
        

    def avoid_obstacle_horizontal(self):
        self.turning_x.insert(0, self.x_turned[len(self.x_turned) - 1])
        self.path_inversion()
        while self.body.getCenter().getX() > self.turning_x[0][0] + 0.5:
            self.body.move(-0.5, 0)
            update(self.speed)

    def avoid_obstacle_vertical(self):
        current_position = (self.body.getCenter().getX(), self.body.getCenter().getY())
        current_row, current_collumn = get_spot(current_position, self.cell_width)
        if current_position[1] >= self.latest_collision.anchor.getY():
            for row in self.grid[:current_row]:
                if row[current_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[current_collumn].x_coord + self.cell_width / 2,
                                   row[current_collumn].y_coord + self.cell_width / 2)
                    break
        else:
            for row in self.grid[current_row:]:
                if row[current_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[current_collumn].x_coord + self.cell_width / 2, 
                                   row[current_collumn].y_coord + self.cell_width / 2)
                    break
        try:
            self.move_with_shortest_path(target)
        except:
            self.path_inversion()
        #target.get_square(self.win)

    def sweep_whole_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()
            self.turning_x = []
            self.x_turned = []
            y_turn = 0.5
            for x in range(100 // (2 * self.radius)):
                self.turning_x.append([(x * 2 + 1) * self.radius, y_turn])
                y_turn *= -1
            if not self.quit:
                while len(self.turning_x) > 0:
                    while self.body.getCenter().getX() < self.turning_x[0][0]:
                        if not self.collision(obstacle_list):
                            if self.collision(dirty_spots):
                                return_spot = self.body.getCenter()
                                spot = self.collision(dirty_spots)[0]
                                self.move(spot.body.getCenter())
                                self.clean_spot()
                                dirty_spots.remove(spot)
                                spot.cleaned()
                                self.move(return_spot)
                            else:
                                self.body.move(0.5, 0)
                        else:
                            self.avoid_obstacle_horizontal()
                        update(self.speed)
                    self.body.move(0, self.turning_x[0][1])
                    while self.radius < self.body.getCenter().getY() < 100 - self.radius:
                        if not self.collision(obstacle_list):
                            if self.collision(dirty_spots):
                                return_spot = self.body.getCenter()
                                spot = self.collision(dirty_spots)[0]
                                self.move(spot.body.getCenter())
                                self.clean_spot()
                                dirty_spots.remove(spot)
                                spot.cleaned()
                                self.move(return_spot)
                            else:
                                self.body.move(0, self.turning_x[0][1])
                        else:
                            self.avoid_obstacle_vertical()
                        update(self.speed)
                    self.x_turned.append(self.turning_x[0])
                    self.turning_x.pop(0)
                    print(self.turning_x)
                    print(self.x_turned)
                
                    # self.clean_dirty_spots(dirty_spots)
                    # self.move_to_docking(docking_stations)
                    # self.start = False
            else:
                break
            self.move_to_docking(docking_stations)
            self.win.getMouse()

