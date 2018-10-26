import Greedy_best_first


# uniform cost search
def search(initial_state, goal_state, yield_after):
    def g(node):
        return node.compute_cost()
    return Greedy_best_first.search(initial_state, goal_state, g, yield_after)
