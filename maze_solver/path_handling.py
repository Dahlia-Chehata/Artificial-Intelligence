import re
import random 


def gamify_policy(policy):
    policy_string = '\n'.join([''.join(row) for row in policy])
    policy_string = re.sub(r'\$', '   $   ', policy_string)
    policy_string = re.sub('up', '   ↑   ', policy_string)
    policy_string = re.sub('down', '   ↓   ', policy_string)
    policy_string = re.sub('right', '   →   ', policy_string)
    policy_string = re.sub('left', '   ←   ', policy_string)
    return policy_string


def rand_st_en(row, char):

    l_i = [x for x in range(7)]
    while True:
        ind = random.choice(l_i)

        if row[ind] == ' ':
            row[ind] = char
            break

def path_cost(maze, policy):

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start_i = i
                start_j = j

    end_i = 1
    end_j = 1

    total_cost = 0

    while start_i != end_i or start_j != end_j:
        
        total_cost += 1

        if policy[start_i][start_j] == 'up':
            start_i -= 1
        elif policy[start_i][start_j] == 'down':
            start_i += 1
        elif policy[start_i][start_j] == 'right':
            start_j += 1
        elif policy[start_i][start_j] == 'left':
            start_j -= 1


    return total_cost


def path_to_goal(maze, policy):

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start_i = i
                start_j = j

    end_i = 1
    end_j = 1

    path_to_goal = []

    while start_i != end_i or start_j != end_j:
        
        path_to_goal.append((start_i, start_j))

        if policy[start_i][start_j] == 'up':
            start_i -= 1
        elif policy[start_i][start_j] == 'down':
            start_i += 1
        elif policy[start_i][start_j] == 'right':
            start_j += 1
        elif policy[start_i][start_j] == 'left':
            start_j -= 1

    path_to_goal.append((start_i, start_j))
    return path_to_goal

def handle_path(maze, policy, l_row):
    # pick random start point from last raw
    rand_st_en(maze[l_row], 'S')
    # pick end point from first raw
    maze[1][1] = 'E'
    # print maze
    print()
    for raw in maze:
        print(raw)
    print()
    #print policy
    policy_str = gamify_policy(policy)
    print(policy_str)
    print()
    #print path data
    print("Path cost is: " + str(path_cost(maze, policy)))
    print("Path to goal is: " + str(path_to_goal(maze, policy)))
    print()