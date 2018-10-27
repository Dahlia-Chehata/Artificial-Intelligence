from Node import Node


def search(initial_state, goal_state, limit, yield_after):
    cur_node = Node(initial_state)
    explored = set()
    stack = list([cur_node])
    counter = 0
    depth = 1
    while stack:
        cur_node = stack.pop()
        depth = max(depth, cur_node.depth)

        explored.add(cur_node.map)
        if cur_node.is_goal(goal_state):
            break
        if cur_node.depth < limit:
            cur_node.expand()
            for child in reversed(cur_node.children):
                if child.map not in explored:
                    stack.append(child)
                    explored.add(child.map)
        else:
            continue
        counter += 1
        if counter % yield_after == 0:
            yield [0, cur_node.state]

    if not cur_node.is_goal(goal_state):
        yield [-1]

    expanded_states = [cur_node.state]
    for parent in cur_node.ancestors():
        expanded_states.append(parent.state)
    expanded_states.reverse()
    yield [1, cur_node.state, expanded_states, counter, depth+1]
