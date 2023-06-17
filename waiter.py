# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 05:20:15 2023

@authors: José Melícias & Vítor Clara
"""

from graphics import *
from math import cos, sin
from shortest_path import *
from universal_functions import *
from obstacles import *
from button import Button

LED_GREEN = color_rgb(17, 207, 48)
LED_BLUE = "blue"
LED_RED = "red"
class Waiter:
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid):
        self.show_grid = show_grid
        self.win = win
        self.radius = radius
        self.docking_stations = docking_stations
        self.anchor = self.docking_stations[0].anchor
        self.tolerance = tolerance
        self.speed = speed
        self.body = Circle(self.anchor, self.radius)
        self.body.setFill(color_rgb(41, 39, 39))
        self.outline = Circle(self.anchor, self.radius * 0.95)
        self.outline.setFill("gray")
        self.quit = False
        self.start = False
        self.cell_width = self.radius / 2
        self.battery = 9500
        self.body_entities = [self.body, self.outline]
        self.get_buttons()

    def grid_show(self):
        if self.show_grid:
            for row in self.grid:
                for spot in row:
                    if spot.ask_obstacle():
                        spot.get_square(self.win, "black")

    def get_buttons(self):
        self.start_button = Button(Point(3, 97.5), Point(
            11, 100), color_rgb(41, 39, 39), color_rgb(184, 162, 125), 
            "Start", color_rgb(41, 39, 39), 13)
        self.quit_button = Button(Point(0, 97.5), Point(3, 100), color_rgb(41, 39, 39), color_rgb(234, 16, 9), "X", 
            color_rgb(41, 39, 39), 13)
        self.buttons = [self.start_button, self.quit_button]
        for button in self.buttons:
            button.body.setWidth(1)
            button.draw(self.win)

    def draw(self):
        for entity in self.body_entities:
            entity.draw(self.win)

    def undraw(self):
        for entity in self.body_entities:
            entity.undraw()

    def get_dirty_spots(self):
        dirty_spots = []
        while not self.start:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                    for spot in dirty_spots:
                        spot.cleaned()
                    self.quit = True
                    break
            if self.start_button.clicked(mouse_click):
                self.start = True
            else:
                path_to_dirt = run_algorithm(self.cell_width, self.grid, (self.body.getCenter().getX(), 
                                            self.body.getCenter().getY()), (mouse_click.getX(), mouse_click.getY()))
                if path_to_dirt == None:
                    display_error_message("O ponto sujo não pode \n interceptar obstáculos", self.win)
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
            self.battery -= 1
            for entity in self.body_entities:
                entity.move(dx, dy)
            update(self.speed)

    def get_vector(self, target):
        delta_x, delta_y, distance = get_distance(
            target, self.body.getCenter())
        dx = delta_x / (distance * 2.5 + 0.01)
        dy = delta_y / (distance * 2.5 + 0.01)
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
            for entity in self.body_entities:
                entity.move(dx, dy)
            theta += 0.30
            spiral += 0.02
            update(self.speed / 2.5)
        

    def move_to_docking(self):
        station_paths = {}
        path_sizes = []
        for station in self.docking_stations:
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
        self.move(self.docking_stations[shortest_index].anchor)

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
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid):
        super().__init__(radius, tolerance, speed, docking_stations, win, show_grid)
        self.grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 2.7, self.cell_width * 1.3, self.cell_width * 2)[0]
        self.grid_show()
        self.draw()


        
    def clean_dirty_spots(self, dirty_spots):
        for spot in dirty_spots:
            spot_center = spot.body.getCenter()
            self.move_with_shortest_path(spot_center)
            self.clean_spot()
            spot.cleaned()



    def clean_room(self):
        while True:
            dirty_spots = self.get_dirty_spots()            
            if not self.quit:
                self.clean_dirty_spots(dirty_spots)
                self.move_to_docking()
                self.start = False
            else:
                for obstacle in obstacle_list:
                    obstacle_list.remove(obstacle)
                break



class Waiter23(Waiter):
    def __init__(self, radius, tolerance, speed, docking_stations, win, show_grid, show_cleaned, dirty_places=[]):
        super().__init__(radius, tolerance, speed, docking_stations, win, show_grid)
        self.dirty_places = dirty_places
        self.show_cleaned = show_cleaned
        self.grid, self.non_obstacle_grid = initialize_algorithm(
            self.cell_width, obstacle_list, self.win, self.cell_width * 2, self.cell_width * 2)
        self.grid_show()
        self.latest_collision = None
        self.charge_led = Circle(self.body.getCenter(), self.radius * 0.35)
        self.charge_led.setFill(LED_GREEN)
        self.body_entities.append(self.charge_led)
        self.draw()

    def get_dirt_from_file(self):
        dirty_spots = []
        for dirt in self.dirty_places:
            dirty_spots.append(Dirt(dirt.anchor, self, self.win))
        while not self.start:
            mouse_click = self.win.getMouse()
            if self.quit_button.clicked(mouse_click):
                for spot in dirty_spots:
                    spot.cleaned()
                self.quit = True
                break
            if self.start_button.clicked(mouse_click):
                self.start = True
        return dirty_spots

    def low_battery(self):
        return_pos = self.body.getCenter()
        self.charge_led.setFill(LED_RED)
        self.move_to_docking()
        self.charge_led.setFill(LED_BLUE)
        time.sleep(2)
        self.battery = 9500
        self.charge_led.setFill(LED_GREEN)
        self.move_with_shortest_path(return_pos)

    def clean_whole_room(self):
        while True:
            if len(self.dirty_places) != 0:
                dirty_spots = self.get_dirt_from_file()
            else:
                dirty_spots = self.get_dirty_spots()
            if not self.quit:
                for row in self.non_obstacle_grid:
                    for spot in row:
                        spot.clean = False
                self.move_through_grid(dirty_spots)
                self.move_to_docking()
                self.start = False
            else:
                for obstacle in obstacle_list:
                    obstacle_list.remove(obstacle)
                break

    
    def move_through_grid(self, dirty_spots):
        for row in self.non_obstacle_grid[3::4]:
            for spot in row:
                for neighbor in spot.neighbors:
                    for second_neighbor in neighbor.neighbors:
                        if self.collision([second_neighbor]):
                            second_neighbor.clean = True
                            if self.show_cleaned:
                                square = second_neighbor.get_square(self.win, "blue")
                if not spot.clean:
                    spot_anchor = (spot.anchor.getX(), spot.anchor.getY())
                    target = Point(
                        spot_anchor[0] + self.cell_width/2, spot_anchor[1] + self.cell_width/2)
                    if self.battery <= 250:
                        self.low_battery()
                    try:
                        self.move_with_shortest_path(target, dirty_spots)
                    except:
                        continue


