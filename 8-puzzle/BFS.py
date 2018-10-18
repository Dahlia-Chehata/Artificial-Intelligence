from Node import Node
from collections import deque


def search(state, goal_state):
    cur_node = Node(state)
    explored = set()
    queue = deque([cur_node])
    while not queue:
        cur_node = queue.popleft()
        explored.add(cur_node.map)
        if cur_node.is_goal(goal_state):
            break
        cur_node.expand()
        for child in cur_node.children:
            if child.map not in explored:
                queue.append(child)
                explored.add(child.map)
    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    return expanded_states
