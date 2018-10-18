from Node import Node


def search(state, goal_state):
    cur_node = Node(state)
    explored = set()
    stack = list([cur_node])
    while stack:
        cur_node = stack.pop()
        explored.add(cur_node.map)
        if cur_node.is_goal(goal_state):
            break
        cur_node.expand()
        for child in reversed(cur_node.children):
            if child.map not in explored:
                stack.append(child)
                explored.add(child.map)
        expanded_states = [cur_node.state]
        for parent in cur_node.ancestors():
            expanded_states.append(parent.state)
        expanded_states.reverse()
        return expanded_states
