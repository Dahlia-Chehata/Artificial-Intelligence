import Greedy_best_first
import heapq
import math


def search(state, goal_state, heuristic_type):
    def g(node):
        return node.compute_cost()
    tiles_indices = []
    for i in range(len(goal_state)):
        for j in range(len(goal_state)):
            heapq.heappush(tiles_indices, (goal_state[i][j], (i, j)))

    def h(node):
        cost = 0
        for i in range(len(node.state)):
            for j in range(len(node.state)):
                tile_i, tile_j = tiles_indices[node.state[i][j]][1]
                if i != tile_i or j != tile_j:
                    if heuristic_type == "Manhattan":
                        cost += abs(tile_i - i) + abs(tile_j - j)
                    elif heuristic_type == "Euclidean Distance":
                        cost += math.sqrt((tile_i - i) * (tile_i - i) + (tile_j - j) * (tile_j - j))
                    else:
                        raise "Not supported heuristic"
        return cost

    def f(node):
        return g(node) + h(node)
    return Greedy_best_first.search(state, goal_state, f)