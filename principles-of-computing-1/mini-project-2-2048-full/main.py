# this project has to be run in codeskulptor.org
"""
Clone of 2048 game.
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
    Function that merges a single row or column in 2048.
    """

    result = slide_zeros(line)
    for num in range(len(result)):

        if num != len(result) - 1:
            if result[num] != 0 and result[num] == result[num + 1]:
                result[num] *= 2
                result[num + 1] = 0
    return slide_zeros(result)


def slide_zeros(line):
    """
    Function that slide non-zero entries to the beginning of list.
    """

    result = [0 for dummy_num in range(len(line))]
    index = 0

    for num in line:
        if num != 0:
            result[index] = num
            index += 1

    return result


def random_tile_value():
    """
    Function to return a random value for a tile
    """
    
    return random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self._height = grid_height
        self._width = grid_width
        self._initial_tiles_indices = {UP: [(0, col) for col in range(self._width)],
                                       DOWN: [(self._height - 1, col) for col in range(self._width)],
                                       LEFT: [(row, 0) for row in range(self._height)],
                                       RIGHT: [(row, self._width - 1) for row in range(self._height)]}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """

        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """

        res = ""
        for idx, val in enumerate(self._grid):
            res += 'row ' + str(idx) + ':' + str(val) + '\n'

        return res

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_moved = False
        for row, col in self._initial_tiles_indices[direction]:
            temp_list_values = []
            temp_list_indices = []
            len_of_list = self._height if direction == UP or direction == DOWN else self._width

            for dummy_num in range(len_of_list):
                    temp_list_values.append(self._grid[row][col])
                    temp_list_indices.append((row, col))
                    row += OFFSETS[direction][0]
                    col += OFFSETS[direction][1]

            temp_list_values = merge(temp_list_values)

            for idx, val in enumerate(temp_list_indices):
                if self._grid[val[0]][val[1]] != temp_list_values[idx]:
                    tile_moved = True

                self._grid[val[0]][val[1]] = temp_list_values[idx]

        if tile_moved:
                self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        while True:
            index = (random.randrange(self._height), random.randrange(self._width))
            if self._grid[index[0]][index[1]] == 0:
                break
        self.set_tile(index[0], index[1],random_tile_value())

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
