import DLS


def search(initial_state, goal_state, yield_after):
    step = [-1]
    depth = 0
    realTotalVisitedNodes = 0

    while step[0] != 1:
        sol = DLS.search(initial_state, goal_state, depth, yield_after, realTotalVisitedNodes)
        for step in sol:
            if step[0] != 1:
                realTotalVisitedNodes = step[2]
            if step[0] == -1:
                break
            yield(step)
        depth += 1