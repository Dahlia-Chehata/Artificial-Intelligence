from maze_utilities import utilities
from maze_utilities import np
from random import choice, randrange

import random

"""
Aldous Broder Algorithm for maze generation
________________________________________
1. Choose a random cell.
2. Choose a random neighbor of the current cell and visit it. 
   If the neighbor has not yet been visited, add the traveled edge to the spanning tree.
3. Repeat step 2 until all cells have been visited.
"""


class Aldous_Broder(utilities):

    def __init__(self, height, width):
        super(Aldous_Broder, self).__init__(height, width)

    def generate(self):
        random.seed(0)

        # create empty grid with barriers
        g = np.empty((self.Height, self.Width), dtype=str)
        g.fill('$')
        grid = g

        cur_row = randrange(1, self.Height, 2)
        cur_col = randrange(1, self.Width, 2)
        grid[cur_row][cur_col] = ' '
        num_visited = 1

        while num_visited < self.height * self.width:
            # find neighbors
            neighbors = self.find_neighbors(cur_row, cur_col, grid, True)

            # if all neighbors have already been visited, choose random neighbor as current cell
            if len(neighbors) == 0:
                (cur_row, cur_col) = choice(self.find_neighbors(cur_row, cur_col, grid))
                continue

            # loop through neighbors
            for neighbor_row, neighbor_col in neighbors:
                # if neighbor is a barrier
                if grid[neighbor_row][neighbor_col] != ' ':
                    # open up barrier to new neighbor
                    grid[(neighbor_row + cur_row) // 2][(neighbor_col + cur_col) // 2] = ' '
                    # mark neighbor as visited
                    grid[neighbor_row][neighbor_col] = ' '
                    num_visited += 1
                    cur_row = neighbor_row
                    cur_col = neighbor_col
                    break
        return grid.tolist()




if __name__ == '__main__':
    test = Aldous_Broder(3, 3).generate()
    print(test)