from queue import PriorityQueue
from graphics import *
from universal_functions import *

class Spot:
    def __init__(self, row, col, cell_width, num_rows):

        self.cell_width = cell_width
        self.width = self.cell_width

        self.row = row
        self.col = col
        self.num_rows = num_rows

        self.x_coord = col*self.width
        self.y_coord = row*self.width

        self.neighbors = []
        self.state = "unchecked"

    def get_coords(self):
        return self.row, self.col
        
    def obstacle_spot(self):
        self.state = "obstacle"

    def ask_obstacle(self):
        return self.state == "obstacle"
        
    def reset(self):
        self.state = "unchecked"

    def get_square(self, win):
        square = Rectangle(Point(self.x_coord, self.y_coord), 
                           Point(self.x_coord + self.width, self.y_coord + self.width))
        square.setOutline("black")
        square.draw(win)

    def update_neighbors(self, grid):
        self.neighbors = []
        self.diagonal_neighbors = []
        # DOWN
        if self.row < self.num_rows - 1 \
        and not grid[self.row + 1][self.col].ask_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
            # DOWN-RIGHT

            if self.col < self.num_rows - 1 \
            and not grid[self.row + 1][self.col + 1].ask_obstacle() \
            and not grid[self.row][self.col + 1].ask_obstacle():
                self.neighbors.append(grid[self.row + 1][self.col + 1])
                self.diagonal_neighbors.append(grid[self.row + 1][self.col + 1])
                # DOWN-LEFT

            if self.col > 0 \
            and not grid[self.row + 1][self.col - 1].ask_obstacle() \
            and not grid[self.row][self.col - 1].ask_obstacle():                    
                self.neighbors.append(grid[self.row + 1][self.col - 1])
                self.diagonal_neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row > 0 \
        and not grid[self.row - 1][self.col].ask_obstacle():  # UP                
            self.neighbors.append(grid[self.row - 1][self.col])
                # UP-RIGHT
            if self.col < self.num_rows - 1 \
            and not grid[self.row - 1][self.col + 1].ask_obstacle() \
            and not grid[self.row][self.col + 1].ask_obstacle():                    
                self.neighbors.append(grid[self.row - 1][self.col + 1])
                self.diagonal_neighbors.append(grid[self.row - 1][self.col + 1])


            if self.col > 0 \
            and not grid[self.row - 1][self.col - 1].ask_obstacle() \
            and not grid[self.row][self.col - 1].ask_obstacle():  # UP-LEFT                    
                self.neighbors.append(grid[self.row - 1][self.col - 1])
                self.diagonal_neighbors.append(grid[self.row - 1][self.col - 1])

            # RIGHT
        if self.col < self.num_rows - 1 \
        and not grid[self.row][self.col + 1].ask_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 \
        and not grid[self.row][self.col - 1].ask_obstacle():  # LEFT                
            self.neighbors.append(grid[self.row][self.col - 1])

    def check_occupation(self, obstacle_list, win):
        occupation = []
        for obstacle in obstacle_list:
            if obstacle.shape == "square":
                if square_square_interception((self.x_coord, self.y_coord), self.width,
                                              (obstacle.anchor.getX(), obstacle.anchor.getY()), 
                                              obstacle.width, self.width * 3):
                    occupation.append(obstacle)
            elif obstacle.shape == "circle":
                if circle_square_interception((self.x_coord, self.y_coord), self.width, 
                                            (obstacle.anchor.getX(), obstacle.anchor.getY()), 
                                            obstacle.radius, self.width * 1.7):
                    occupation.append(obstacle)
                    
        if len(occupation) != 0:
            self.obstacle_spot()
            #self.get_square(win)
            
                        
        
def grid_maker(window_size, cell_width):
    cell_width = cell_width
    num_rows = window_size // cell_width
    grid = []
    for row in range(int(num_rows)):
        grid.append([]) 
        for col in range(int(num_rows)):
            spot = Spot(row, col, cell_width, num_rows)
            grid[row].append(spot)
    return grid


def h_value(p_A, p_B):
    x_A, y_A = p_A
    x_B, y_B = p_B
    h_value = abs(x_A - x_B) + abs(y_A - y_B)
    return h_value


def grid_maker(window_size, cell_width):
    cell_width = cell_width
    num_rows = window_size // cell_width
    grid = []
    for row in range(int(num_rows)):
        grid.append([])
        for col in range(int(num_rows)):
            spot = Spot(row, col, cell_width, num_rows)
            grid[row].append(spot)
    return grid

def algorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_value = {spot: float("inf") for row in grid for spot in row}
    g_value[start] = 0
    f_value = {spot: float("inf") for row in grid for spot in row}

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_to_dirt = []
            while current in came_from:
                current = came_from[current]
                path_to_dirt.insert(0, current)
            return path_to_dirt
        
        for neighbor in current.neighbors:
            if neighbor not in current.diagonal_neighbors:
                temp_g_value = g_value[current] + 1
            else:
                temp_g_value = g_value[current] + 1.4

            if temp_g_value < g_value[neighbor]:
                came_from[neighbor] = current
                g_value[neighbor] = temp_g_value
                f_value[neighbor] = temp_g_value + \
                    h_value(neighbor.get_coords(), end.get_coords())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_value[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)


def get_spot(point, cell_width):
    spot_width = cell_width
    x, y = point[0], point[1]
    row = int(y // spot_width)
    col = int(x // spot_width)
    return row, col

def initialize_algorithm(cell_width, obstacle_list, win):
        grid = grid_maker(100, cell_width)
        for row in grid:
            for spot in row:
                spot.check_occupation(obstacle_list, win)
        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)
        return grid
    

def run_algorithm(cell_width, grid, start_point, end_point): 
    row_start, col_start = get_spot(start_point, cell_width)
    row_end, col_end = get_spot(end_point, cell_width)
    start = grid[row_start][col_start]
    end = grid[row_end][col_end]
    path_to_dirt = algorithm(grid, start, end)
    return path_to_dirt
