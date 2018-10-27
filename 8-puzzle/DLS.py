from Node import Node
from collections import deque


def search(initial_state, goal_state, limit, yield_after, counter):
    cur_node = Node(initial_state)
    explored = set()
    queue = deque([cur_node])
    depth = 0
    while queue:
        cur_node = queue.popleft()

        if cur_node.depth >= limit:
            continue;

        depth = max(depth, cur_node.depth)
        explored.add(cur_node.map)
        if cur_node.is_goal(goal_state):
            break

        cur_node.expand()
        for child in reversed(cur_node.children):
            if child.map not in explored:
                queue.append(child)
                explored.add(child.map)

        counter += 1
        if counter % yield_after == 0:
            yield [0, cur_node.state, counter]

    if not cur_node.is_goal(goal_state):
        yield [-1, -1, counter]

    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    yield [1, cur_node.state, expanded_states, counter, depth+1]
