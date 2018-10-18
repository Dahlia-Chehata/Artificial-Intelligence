import heapq
from Node import Node


def search(state, goal_state, heuristic):
    cur_node = Node(state)
    frontier = [(heuristic(cur_node), 0, cur_node)]
    index = 1
    while frontier:
        cur_node = heapq.heappop(frontier)[2]
        if cur_node.is_goal(goal_state):
            break
        cur_node.expand()
        for child in cur_node.children:
            item = (heuristic(child), index, child)
            heapq.heappush(frontier, item)
            index += 1
    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    return expanded_states
