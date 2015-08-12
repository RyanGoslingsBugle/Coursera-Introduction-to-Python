"""
Clone of 2048 game. Must be run inside Codeskulptor environment: http://www.codeskulptor.org/
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    new_line = []
    temp_index = 0
    merged_list = []
    for dummy_iter in range(len(line)):
        new_line.append(0)
        merged_list.append(False)
        if line[dummy_iter] != 0:
            new_line[temp_index] = line[dummy_iter]
            if temp_index >= 1 and merged_list[temp_index - 1] == False:
                if new_line[temp_index] == new_line[temp_index - 1]:
                    new_line[temp_index - 1] *= 2
                    new_line[temp_index] = 0
                    temp_index -= 1
                    merged_list[temp_index] = True
            temp_index += 1
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
       
    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.tiles = {}
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                    self.tiles[row,col] = 0
        self.initial_tiles = {UP:[],DOWN:[],LEFT:[],RIGHT:[]}      
        for col in range(self.grid_width):
                self.initial_tiles[UP].append((0, col))
                self.initial_tiles[DOWN].append((self.grid_height - 1, col))
        for row in range(self.grid_height):
                self.initial_tiles[LEFT].append((row, 0))
                self.initial_tiles[RIGHT].append((row, self.grid_width - 1))
        
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                    self.tiles[(row,col)] = 0
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        temp_string = ""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                temp_string += str(self.tiles[(row,col)])
            temp_string += "    "
        return temp_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return int(self.grid_height)
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return int(self.grid_width)
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        shift = list(OFFSETS[direction])
        changed = False
        for tile in self.initial_tiles[direction]:
            temp_list = []
            temp_list.append(self.tiles[tile])
            if direction < 3:
                for dummy_iter in range(1, self.grid_height):
                    temp_list.append(self.tiles[tile[0] + shift[0] * dummy_iter, tile[1]])
            else:
                for dummy_iter in range(1, self.grid_width):
                    temp_list.append(self.tiles[tile[0], tile[1] + shift[1] * dummy_iter])
            temp_list = merge(temp_list)
            if direction < 3:
                for dummy_iter in range(self.grid_height):
                    if temp_list[dummy_iter] != self.tiles[tile[0] + shift[0] * dummy_iter, tile[1]]:
                        changed = True
                    self.set_tile(tile[0] + shift[0] * dummy_iter, tile[1], temp_list[dummy_iter])
            else:
                for dummy_iter in range(self.grid_width):
                    if temp_list[dummy_iter] != self.tiles[tile[0], tile[1] + shift[1] * dummy_iter]:
                        changed = True
                    self.set_tile(tile[0], tile[1] + shift[1] * dummy_iter, temp_list[dummy_iter])
        if changed:
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randrange(self.grid_height)
        col = random.randrange(self.grid_width)
        while self.tiles[(row,col)] != 0:
            row = random.randrange(self.grid_height)
            col = random.randrange(self.grid_width)
        if random.randrange(10) == 0:
            value = 4
        else:
            value = 2
        self.tiles[(row,col)] = value
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.tiles[(row,col)] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.tiles[row,col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))