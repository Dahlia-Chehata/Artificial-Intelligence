import abc
from numpy.random import shuffle
import numpy as np


def is_barrier(char):
    return not(char == ' ')


class utilities(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, height, width):
        if width < 3 or height < 3:
            raise ValueError('maze smaller than 3x3 is not allowed.')
        self.height = height
        self.width = width
        self.Height = (2 * self.height) + 1
        self.Width = (2 * self.width) + 1

    @abc.abstractmethod
    def generate(self):
        return None

    """ Find all neighbors of the current position in the grid
    """
    def find_neighbors(self, row, col, grid, barrier=False):

        ns = []

        if row > 1 and is_barrier(grid[row - 2][col]) == barrier:
            ns.append((row - 2, col))
        if row < self.Height - 2 and is_barrier(grid[row + 2][col]) == barrier:
            ns.append((row + 2, col))
        if col > 1 and is_barrier(grid[row][col - 2]) == barrier:
            ns.append((row, col - 2))
        if col < self.Width - 2 and is_barrier(grid[row][col + 2]) == barrier:
            ns.append((row, col + 2))

        shuffle(ns)

        return ns
