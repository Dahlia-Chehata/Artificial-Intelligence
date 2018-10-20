import heapq
from Node import Node


def search(state, goal_state, heuristic):
    cur_node = Node(state)
    frontier = [(heuristic(cur_node), 0, cur_node)]
    
    explored_set = set()
    forntier_set = set()
    forntier_set.add(cur_node.map)

    index = 1
    while frontier:
        cur_node = heapq.heappop(frontier)[2]

        explored_set.add(cur_node.map)
        forntier_set.remove(cur_node.map)

        if cur_node.is_goal(goal_state):
            break
        cur_node.expand()
        for child in cur_node.children:
            if child.map not in explored_set and child.map not in forntier_set:
                forntier_set.add(child.map)
                item = (heuristic(child), index, child)
                heapq.heappush(frontier, item)
                index += 1

    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    return expanded_states
