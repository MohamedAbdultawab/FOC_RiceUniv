"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
# this project has to be run in codeskulptor.org
# An online version could be found here: http://www.codeskulptor.org/#user44_oz8YRyH9CI_0.py


import poc_fifteen_gui


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid is not None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] == 0:
            for col in range(target_col + 1, self.get_width()):
                if self.current_position(target_row, col) == (target_row, col):
                    continue
                return False
            for row in range(target_row + 1, self.get_height()):
                for col in range(self.get_width()):
                    if self.current_position(row, col) == (row, col):
                        continue
                    return False
            return True
        return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1
        assert target_col > 0
        assert self.lower_row_invariant(target_row, target_col)
        oppsite = {'l': 'r', 'r': 'l', 'u': 'd', 'd': 'u'}

        def position_on_row(zero_pos, target_pos, direction, target_dir):
            """
            if row = 0 direction will be 'd' else will be 'u'
            target_dir will be 'l' when target_pos is on the left side of zero_pos, 'r' otherwise
            :param zero_pos: position of tile zero
            :param target_pos: position of the targeted position on the same row
            :return: move string
            """
            move = ''
            width = abs(target_pos[1] - zero_pos[1])
            if width == 1:
                move += target_dir
                return move
            move += (target_dir * width) + direction + (oppsite[target_dir] * width) + oppsite[direction]
            if target_dir == 'l':
                move += position_on_row(zero_pos, (target_pos[0], target_pos[1] + 1), direction, target_dir)
            else:
                move += position_on_row(zero_pos, (target_pos[0], target_pos[1] - 1), direction, target_dir)
            return move

        def position_on_col(zero_pos, target_pos):
            """

            :param zero_pos:
            :param target_pos:
            :return:
            """
            move = ''
            height = zero_pos[0] - target_pos[0]
            if height == 1:
                move += 'u'
                return move
            move += ('u' * height) + 'l' + ('d' * height) + 'r' + position_on_col(zero_pos,
                                                                                (target_pos[0] + 1, target_pos[1]))
            return move

        target_pos = self.current_position(target_row, target_col)
        zero_pos = (target_row, target_col)
        move = ''
        if target_pos[0] == zero_pos[0]:
            if target_pos[0] == 0:
                if target_pos[1] - zero_pos[1] < 0:
                    move += position_on_row(zero_pos, target_pos, 'd', 'l')
                else:
                    move += position_on_row(zero_pos, target_pos, 'd', 'r')
            else:
                if target_pos[1] - zero_pos[1] < 0:
                    move += position_on_row(zero_pos, target_pos, 'u', 'l')
                else:
                    move += position_on_row(zero_pos, target_pos, 'u', 'r')
        else:
            if target_pos[1] == zero_pos[1]:
                move += position_on_col(zero_pos, target_pos)
                move += 'ld'
            else:
                height = zero_pos[0] - target_pos[0]

                move += ('u' * height)
                if target_pos[0] == 0:
                    if target_pos[1] - zero_pos[1] < 0:
                        move += position_on_row((target_pos[0], zero_pos[1]), target_pos, 'd', 'l')
                        move += ('d' * height) + 'r' + position_on_col(zero_pos, (target_pos[0], zero_pos[1]))
                        move += 'ld'
                    else:
                        move += position_on_row((zero_pos[0] - height, zero_pos[1]), target_pos, 'd', 'r')
                        move += ('d' * (height - 1)) + 'ld' + position_on_col(zero_pos, (target_pos[0], zero_pos[1]))
                        move += 'l' + ('d' * (height - 1))
                else:
                    if target_pos[1] - zero_pos[1] < 0:
                        move += position_on_row((zero_pos[0] - height, zero_pos[1]), target_pos, 'u', 'l')
                        move += ('d' * height) + 'r' + position_on_col(zero_pos, (target_pos[0], zero_pos[1]))
                        move += 'ld'
                    else:
                        move += position_on_row((zero_pos[0] - height, zero_pos[1]), target_pos, 'u', 'r')
                        move += 'u' + ('l' * ((target_pos[1] - zero_pos[1]) + 1)) \
                                + ('d' * (height + 1)) + 'r' + position_on_col(zero_pos, (target_pos[0], zero_pos[1]))
                        move += 'l' + ('d' * height)

        clone = self.clone()
        clone.update_puzzle(move)
        assert clone.lower_row_invariant(target_row, target_col - 1)
        self.update_puzzle(move)
        return move

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        def position_on_row(zero_pos, target_pos):
            """
            return: move string
            """
            move = ''
            if zero_pos[0] - target_pos[0] == 2:
                move += 'u' + ('r' * target_pos[1]) + 'u' + ('l' * target_pos[1]) + 'd'
                return move

            height = zero_pos[0] - target_pos[0]
            move += 'u' + ('r' * target_pos[1]) + ('u' * (height - 1)) + ('l' * target_pos[1]) + ('d' * height) 
            move += position_on_row(zero_pos, (target_pos[0] +1, target_pos[1]))
            return move

        def position_on_col(zero_pos, target_pos):
            """

            :param zero_pos:
            :param target_pos:
            :return:
            """
            move = ''
            if target_pos[1] - zero_pos[1] == 1:
                move += 'rulld'
                return move
            move += 'r' + position_on_col((zero_pos[0], zero_pos[1] + 1), target_pos)
            return move

        def position_on_col2(target_pos):
            """
            return move string
            """
            width = target_pos[1] - 1
            move = 'r' * (width)
            for dummy in range(width):
                move += 'rulld'
            return move

        target_pos = self.current_position(target_row, 0)
        zero_pos = (target_row, 0)
        move = ''
        if target_pos[0] == target_row - 1 and target_pos[1] == 0:
            move += 'u'
            move += ('r' * (self.get_width() - 1))
            clone = self.clone()
            clone.update_puzzle(move)
            assert clone.lower_row_invariant(target_row - 1, self.get_width() - 1)
            self.update_puzzle(move)
            return move

        else:
            if target_pos[0] == target_row - 1:
                if not target_pos[1] == 1:
                    move += 'ur' + position_on_col(zero_pos, target_pos)
                    move += 'ruldrdlurdluurddlur' + ('r' * (self.get_width() - 2))
                    clone = self.clone()
                    clone.update_puzzle(move)
                    assert clone.lower_row_invariant(target_row - 1, self.get_width() - 1)
                    self.update_puzzle(move)
                    return move
                else:
                    move += 'uruldrdlurdluurddlur' + ('r' * (self.get_width() - 2))
                    clone = self.clone()
                    clone.update_puzzle(move)
                    assert clone.lower_row_invariant(target_row - 1, self.get_width() - 1)
                    self.update_puzzle(move)
                    return move
            else:
                if target_pos[1] != 0:
                    move += position_on_row(zero_pos, target_pos)
                    move += position_on_col2((zero_pos[0] - 1, target_pos[1]))
                    move += 'ruldrdlurdluurddlur' + ('r' * (self.get_width() - 2))
                    clone = self.clone()
                    clone.update_puzzle(move)
                    assert clone.lower_row_invariant(zero_pos[0] - 1, self.get_width() - 1)
                    self.update_puzzle(move)
                    return move
                else:
                    move += 'ur' + ('u' * (zero_pos[0] - target_pos[0] - 1)) + 'l' + ('d' * (zero_pos[0] - target_pos[0]))
                    move += 'ruldrdlurdluurddlur' + ('r' * (self.get_width() - 2))
                    clone = self.clone()
                    clone.update_puzzle(move)
                    assert clone.lower_row_invariant(target_row - 1, self.get_width() - 1)
                    self.update_puzzle(move)
                    return move


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[0][target_col] == 0:
            for col in range(target_col + 1, self.get_width()):
                if self.current_position(0, col) == (0, col):
                    continue
                return False
            clone = self.clone()
            if target_col == 0:
                if self.get_number(1, 0) == self.get_width():
                    clone.update_puzzle('d')
                    return clone.row1_invariant(0)
            clone.update_puzzle('ld')
            return clone.row1_invariant(target_col - 1)
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[1][target_col] == 0:
            for col in range(target_col + 1, self.get_width()):
                if self.current_position(1, col) == (1, col):
                    continue
                return False
            clone = self.clone()
            clone.update_puzzle('r' * (self.get_width() - 1 - target_col))
            return clone.lower_row_invariant(1, self.get_width() - 1)
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        def position_on_row(zero_pos, target_pos):
            """
            return: move string
            """
            move = ''
            width = abs(target_pos[1] - zero_pos[1])
            if width == 1:
                move += 'l'
                return move
            move += ('l' * width) + 'u' + ('r' * width) + 'd'
            move += position_on_row(zero_pos, (target_pos[0], target_pos[1] + 1))
            return move

        move = ''
        zero_pos = (0, target_col)
        target_pos = self.current_position(*zero_pos)
        if target_pos[1] == target_col - 1:
            if target_pos[0] == 0:
                move += 'ld'
            elif target_pos[0] == 1:
                move += 'lld'
                move += 'urdlurrdluldrruld'
        else:
            move += 'ld'
            if target_pos[0] == 0:
                width = abs(target_pos[1] - (target_col -1))
                move += ('l' * width) + 'u' + ('r' * width) + 'd'
            move += position_on_row((1, target_col - 1), (1, target_pos[1]))
            move += 'urdlurrdluldrruld'
        
        clone = self.clone()
        clone.update_puzzle(move)
        assert clone.row1_invariant(target_col - 1)
        self.update_puzzle(move)
        return move


    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        def position_on_row(zero_pos, target_pos):
            """
            return: move string
            """
            move = ''
            width = abs(target_pos[1] - zero_pos[1])
            if width == 1:
                move += 'l'
                return move
            move += ('l' * width) + 'u' + ('r' * width) + 'd'
            move += position_on_row(zero_pos, (target_pos[0], target_pos[1] + 1))
            return move

        zero_pos = (1, target_col)
        target_pos = self.current_position(*zero_pos)
        move = ''
        if target_pos[0] == 1:
            move += position_on_row(zero_pos, target_pos) + 'ur'
        elif target_pos[1] == zero_pos[1]:
            move += 'u'
        else:
            width = zero_pos[1] - target_pos[1]
            move += ('l' * width) + 'u' + ('r' * width) + 'd'
            move += position_on_row(zero_pos, (1, target_pos[1])) + 'ur'

        clone = self.clone()
        clone.update_puzzle(move)
        assert clone.row0_invariant(target_col)
        self.update_puzzle(move)
        return move



    ###########################################################
    # Phase 3 methods

    def is_solved(self):
        """Indicates whether the 2x2 puzzle is solved
        """
        if self.get_number(0, 1) == 1 \
            and self.get_number(1, 0) == self.get_width() \
                and self.get_number(1, 1) == (self.get_width() + 1):
                    return True
        return False


    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1)
        clone = self.clone()
        move = 'lu'
        clone.update_puzzle(move)
        while not clone.is_solved():
            move += 'rdlu'
            clone.update_puzzle('rdlu')

        clone = self.clone()
        clone.update_puzzle(move)
        assert clone.is_solved()
        self.update_puzzle(move)
        return move

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move = ''
        zero_pos = self.current_position(0, 0)
        start_pos = (self.get_height() - 1, self.get_width() -1)
        width = start_pos[1] - zero_pos[1]
        height = start_pos[0] - zero_pos[0]
        move += ('r' * width) + ('d' * height)
        self.update_puzzle(move)
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, 0, -1):
                move += self.solve_interior_tile(row, col)
                assert self.lower_row_invariant(row, col - 1)
            move += self.solve_col0_tile(row)
            assert self.lower_row_invariant(row - 1, self.get_width() - 1)
        for col in range(self.get_width() - 1, 1, -1):
            move += self.solve_row1_tile(col)
            move += self.solve_row0_tile(col)
        move += self.solve_2x2()
        return move



# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]]))
#x = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#x.update_puzzle('rrrrduulldrrulddruulddrulduulllldrrrrullldrrrulldrrulddruulddruldllurrdlullurrdldrulduurrrdlllurrdllurdlduulddruldurrulldrrulldruldrdlurdluurddlurrrrrlllllurrrrrdlllllurrrrrdllllurrrrdlllurrrdllurrdlur')
#poc_fifteen_gui.FifteenGUI(x)
#x.solve_row0_tile(5)
