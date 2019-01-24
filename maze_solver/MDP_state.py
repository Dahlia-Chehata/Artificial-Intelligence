from copy import deepcopy

class MDP_state:

    """
    MDP_state has 4 attributes that point to other squares in the grid. Each attribute is represented by a point (x,y)
    """

    def __init__(self, up, down, left, right, reward=-1, value=0):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.reward = reward
        self.value = value

    def __str__(self):
        return str(self.value)


"""
Returns a matrix of MDPState objects for each free space in a maze
"""


def convert_to_MDP(maze):

    grid = deepcopy(maze)
    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[i]) - 1):

            # represent walls as #
            if maze[i][j] == '$':
                grid[i][j] = '$'
                continue
            # up
            if maze[i - 1][j] == '$':
                north = (i, j)
            else:
                north = (i - 1, j)
            # down
            if maze[i + 1][j] == '$':
                south = (i, j)
            else:
                south = (i + 1, j)
            # left
            if maze[i][j + 1] == '$':
                east = (i, j)
            else:
                east = (i, j + 1)
            # right
            if maze[i][j - 1] == '$':
                west = (i, j)
            else:
                west = (i, j - 1)

            grid[i][j] = MDP_state(north, south, west, east)

    grid[1][1].reward = 10
    return grid
