from copy import deepcopy


class Node:
    def __init__(self, state=None, parent=None, depth=0, cost=0, children=[]):
        self.state = state
        self.children = children
        self.parent = parent
        self.depth = depth
        self.cost = cost
        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    # return the path to the current node
    def ancestors(self):
        cur_node = self
        while cur_node.parent:
            yield cur_node.parent  # to return a generator
            cur_node = cur_node.parent

    # compute g(n) of the node
    def compute_cost(self):
        # costs = self.cost
        # for parent in self.ancestors():
        #     costs += parent.cost
        # return costs
        return self.cost
        
    # compare every square tile in the current board state with those ih the goal state
    def is_goal(self, goal_state):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if self.state[i][j] != goal_state[i][j]:
                    return False
        return True

    # expand function append the valid nodes in the children list of the current node
    def expand(self):
        states_list = move_blank_tile(self.state)
        self.children = []
        for board_state in states_list:
            self.children.append(Node(board_state, self, self.depth + 1, self.cost + 1))


def move_blank_tile(state):
    # to store each board state after every move
    states_list = []
    # to locate the blank tile
    blank_i = 0
    blank_j = 0
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                blank_i = i
                blank_j = j
                break

    # swap blank tile with those in the 4 directions and add to state_list
    def helper(y, x):
        clone = deepcopy(state)
        clone[y][x], clone[blank_i][blank_j] = clone[blank_i][blank_j], clone[y][x]
        states_list.append(clone)

    if blank_i != 0:
        helper(blank_i - 1, blank_j)  # left
    if blank_i != len(state) - 1:
        helper(blank_i + 1, blank_j)  # right
    if blank_j != 0:
        helper(blank_i, blank_j - 1)  # up
    if blank_j != len(state) - 1:
        helper(blank_i, blank_j + 1)  # down
    return states_list
