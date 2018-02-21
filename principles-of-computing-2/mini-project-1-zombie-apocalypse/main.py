# this project has to be run in codeskulptor.org
"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        dist_field = [[self.get_grid_width() * self.get_grid_height()
                       for dummy_col in range(self.get_grid_width())]
                      for dummy_row in range(self.get_grid_height())]
        # Create boundry depending on the entity whether it's a human or zombie
        entity_list = self._human_list if entity_type == HUMAN else self._zombie_list
        boundary = poc_queue.Queue()

        for entity in entity_list:
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            dist_field[entity[0]][entity[1]] = 0

        while boundary:
            current_cell = boundary.dequeue()
            for cell in self.four_neighbors(current_cell[0], current_cell[1]):
                if visited.is_empty(cell[0], cell[1]) and self.is_empty(cell[0], cell[1]):
                    visited.set_full(cell[0], cell[1])
                    boundary.enqueue(cell)
                    dist_field[cell[0]][cell[1]] = dist_field[current_cell[0]][current_cell[1]] + 1
        return dist_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_list = []
        for human in self.humans():
            max_dist_loc = []
            max_dist = 0
            for neighbor in (self.eight_neighbors(human[0], human[1]) + [human]):
                if self.is_empty(neighbor[0], neighbor[1]):
                    if zombie_distance_field[neighbor[0]][neighbor[1]] == max_dist:
                        max_dist_loc.append(neighbor)
                    elif zombie_distance_field[neighbor[0]][neighbor[1]] > max_dist:
                        max_dist = zombie_distance_field[neighbor[0]][neighbor[1]]
                        max_dist_loc = [neighbor]
            human_list.append(random.choice(max_dist_loc))
        self._human_list = human_list

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_list = []
        for zombie in self.zombies():
            min_dist_loc = []
            min_dist = float('inf')
            for neighbor in (self.four_neighbors(zombie[0], zombie[1]) + [zombie]):
                if self.is_empty(neighbor[0], neighbor[1]):
                    if human_distance_field[neighbor[0]][neighbor[1]] == min_dist:
                        min_dist_loc.append(neighbor)
                    elif human_distance_field[neighbor[0]][neighbor[1]] < min_dist:
                        min_dist = human_distance_field[neighbor[0]][neighbor[1]]
                        min_dist_loc = [neighbor]
            zombie_list.append(random.choice(min_dist_loc))
        self._zombie_list = zombie_list


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))
