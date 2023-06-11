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
            self.cell_width, obstacle_list, self.win, self.cell_width * 2, self.cell_width)
        self.latest_collision = None

    def clean_whole_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()
            for row in self.non_obstacle_grid:
                for spot in row:
                    spot.clean = False
            for row in self.non_obstacle_grid[3::6]:
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
            self.win.getMouse()

    def path_inversion(self):
        self.avoidance_count += 1
        print(self.avoidance_count)
        for point in self.turning_x:
            point[1] *= -1
        self.body.move(0, self.turning_x[0][1])
        

    def avoid_obstacle_horizontal(self, dirty_spots):
        #self.turning_x.insert(0, self.x_turned[len(self.x_turned) - 1])
        #self.path_inversion()
        #while self.body.getCenter().getX() > self.turning_x[0][0] + 0.5:
        #    self.body.move(-0.5, 0)
        #    update(self.speed)
        #self.win.getMouse()
        current_position = (self.body.getCenter().getX(),
                            self.body.getCenter().getY())
        temp_row, temp_collumn = get_spot((self.turning_x[0][0], current_position[1]), self.cell_width)       
        if self.latest_collision.body.getCenter().getY() >= 50:
            inverted_row_list = []
            for row in self.grid[:temp_row - 1]:
                inverted_row_list.insert(0, row)
            for row in inverted_row_list:
                if row[temp_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[temp_collumn].x_coord + self.cell_width / 2,
                                   row[temp_collumn].y_coord + self.cell_width / 2)
                    break
        else:
            for row in self.grid[temp_row + 1:]:
                if row[temp_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[temp_collumn].x_coord + self.cell_width / 2,
                                   row[temp_collumn].y_coord + self.cell_width / 2)
                    break
        self.move_with_shortest_path(target, dirty_spots)

    def avoid_obstacle_vertical(self, dirty_spots):
        current_position = (self.body.getCenter().getX(), self.body.getCenter().getY())
        current_row, current_collumn = get_spot(current_position, self.cell_width)
        if current_position[0] <= 3 * self.radius:
            self.move(Point(current_position[0], 100 - self.radius))
        elif current_position[1] >= self.latest_collision.anchor.getY():
            inverted_row_list = []
            for row in self.grid[:current_row - 1]:
                inverted_row_list.insert(0, row)
            for row in inverted_row_list:
                if row[current_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[current_collumn].x_coord + self.cell_width / 2,
                                   row[current_collumn].y_coord + self.cell_width / 2)
                    break
        else:
            for row in self.grid[current_row + 1:]:
                if row[current_collumn].ask_obstacle():
                    continue
                else:
                    target = Point(row[current_collumn].x_coord + self.cell_width / 2, 
                                   row[current_collumn].y_coord + self.cell_width / 2)
                    break
        try:
            #target.get_square(self.win)
            self.move_with_shortest_path(target, dirty_spots)
        except:
            print("Unable to vertically contour")
            if self.avoidance_count <= 4:
                self.path_inversion()
            else:
                self.avoid_obstacle_horizontal(dirty_spots)
        #target.get_square(self.win)

    def sweep_whole_room(self, docking_stations):
        while True:
            dirty_spots = self.get_dirty_spots()
            if not self.collision([docking_stations[0]]):
                self.move_with_shortest_path(docking_stations[0].body.getCenter())
            self.turning_x = []
            self.x_turned = []
            y_turn = 0.25
            for x in range(100 // (2 * self.radius)):
                self.turning_x.append([(x * 2 + 1) * self.radius, y_turn])
                y_turn *= -1
            if not self.quit:
                while len(self.turning_x) > 0:
                    self.avoidance_count = 0
                    while self.body.getCenter().getX() < self.turning_x[0][0]:
                        if not self.collision(obstacle_list):
                            if self.collision(dirty_spots):
                                return_spot = self.body.getCenter()
                                spot = self.latest_collision
                                self.move(spot.body.getCenter())
                                self.clean_spot()
                                dirty_spots.remove(spot)
                                spot.cleaned()
                                self.move(return_spot)
                            else:
                                self.body.move(0.25, 0)
                        else:
                            self.avoid_obstacle_horizontal(dirty_spots)
                        update(self.speed)
                    self.body.move(0, self.turning_x[0][1])
                    while self.radius < self.body.getCenter().getY() < 100 - self.radius:
                        if not self.collision(obstacle_list):
                            if self.collision(dirty_spots):
                                return_spot = self.body.getCenter()
                                spot = self.latest_collision
                                self.move(spot.body.getCenter())
                                self.clean_spot()
                                dirty_spots.remove(spot)
                                spot.cleaned()
                                self.move(return_spot)
                            else:
                                self.body.move(0, self.turning_x[0][1])
                        else:
                            self.avoid_obstacle_vertical(dirty_spots)
                        update(self.speed)
                    self.x_turned.append(self.turning_x[0])
                    self.turning_x.pop(0)
                
                    # self.clean_dirty_spots(dirty_spots)
                    # self.move_to_docking(docking_stations)
                    # self.start = False

                #self.move_to_docking(docking_stations)
                #self.win.getMouse()
            else:
                break
            self.move_to_docking(docking_stations)
            self.start = False

