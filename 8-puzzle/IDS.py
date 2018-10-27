import DLS


def search(initial_state, goal_state, yield_after):
    depth = 0
    sol = None
    while sol is None:
        sol = DLS.search(initial_state, goal_state, depth, yield_after)
        depth += 1
        print(sol)
    return sol
    # expanded_states = [sol.state]
    # for parent in sol.ancestors():
    #     expanded_states.append(parent.state)
    # expanded_states.reverse()
