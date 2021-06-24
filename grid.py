import numpy as np
import pygame as pg

class Grid:
    # Initialize a grid of specific size.
    def __init__(self, CELL_SIZE, CELLS_X, CELLS_Y):
        self.CELL_SIZE = CELL_SIZE
        self.CELLS_X = CELLS_X
        self.CELLS_Y = CELLS_Y
        self.WIDTH, self.HEIGHT = (CELLS_X * CELL_SIZE), (CELLS_Y * CELL_SIZE)

        self.grid_size = (CELLS_X, CELLS_Y)
        self.grid_array = np.ndarray(shape = self.grid_size)
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                self.grid_array[x, y] = False

    # Return the state of a cell given its coordinates.
    is_alive = lambda self, x, y: self.grid_array[x,y]

    # Generate and return the next generation of the grid.
    def next_generation(self):
        g = Grid(self.CELL_SIZE, self.CELLS_X, self.CELLS_Y)
        for x in range(0, self.CELLS_X):
            for y in range(0, self.CELLS_Y):
                neighbors = self.get_alive_neighbors(x,y)
                g.grid_array[x,y] = self.is_alive(x,y)
                if (self.is_alive(x,y) and (neighbors < 2 or neighbors > 3)) or (not self.is_alive(x,y) and neighbors == 3):
                    g.toggle_alive(x,y)
        return g

    # Toggle the state of a cell given its coordinates.
    def toggle_alive(self, x, y):
        self.grid_array[x,y] = not self.grid_array[x,y]

    # Return the number of alive neighbors of a cell given its coordinates.
    def get_alive_neighbors(self, x, y):
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                a, b = x + i, y + j
                if a >= 0 and a < self.CELLS_X and b >= 0 and b < self.CELLS_Y and self.is_alive(a,b) and (a,b) != (x,y):
                    counter += 1
        return counter

    # Given a Pygame surface and color, draw the grid on the surface.
    def draw(self, surface, color):
        for x in range(0, self.CELLS_X):
            for y in range(0, self.CELLS_Y):
                pos_x = x * self.CELL_SIZE
                pos_y = y * self.CELL_SIZE
                border = 0 if self.is_alive(x,y) else 1
                rect = pg.Rect(pos_x, pos_y, self.CELL_SIZE, self.CELL_SIZE)
                pg.draw.rect(surface, color, rect, border)