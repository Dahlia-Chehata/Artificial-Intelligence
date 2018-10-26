import heapq
from Node import Node




def search(state, goal_state, heuristic, yield_after):
    cur_node = Node(state)
    frontier = [(heuristic(cur_node), 0, cur_node)]

    explored_set = set()
    forntier_set = set()
    forntier_set.add(cur_node.map)

    # map a state.map to cost
    cost_so_far = {}
    cost_so_far[cur_node.map] = 0

    index = 1
    counter = 0
    depth = 1
    while frontier:

        # get the highest priority
        cur_node = heapq.heappop(frontier)[2]
        depth = max(depth, cur_node.depth)

        # if already visited, then continue
        if cur_node.map in explored_set:
            continue

        # add the state to explored_set and remove it from forntier_set
        explored_set.add(cur_node.map)
        forntier_set.remove(cur_node.map)

        # if goal, then we are done.
        if cur_node.is_goal(goal_state):
            break

        # else add all the childs
        cur_node.expand()
        for child in cur_node.children:
            # don't add if already visited
            if child.map in explored_set:
                continue
            # add if not visited or has lower cost
            if (child.map in forntier_set and cost_so_far[child.map] > child.cost) or child.map not in forntier_set:
                cost_so_far[child.map] = child.cost
                forntier_set.add(child.map)
                item = (heuristic(child), index, child)
                heapq.heappush(frontier, item)
                index += 1
        counter += 1
        if counter % yield_after == 0:
            yield [0, cur_node.state]
    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    yield [1, cur_node.state, expanded_states, counter, depth+1]
