import DLS


def search(initial_state, goal_state, yield_after):
    depth = 0
    sol = None
    while not sol:
        sol = DLS.search(initial_state, goal_state, depth, yield_after)
        depth += 1
    return sol
    # expanded_states = [sol.state]
    # for parent in sol.ancestors():
    #     expanded_states.append(parent.state)
    # expanded_states.reverse()
