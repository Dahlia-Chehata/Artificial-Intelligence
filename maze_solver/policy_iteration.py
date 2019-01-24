from maze_generator import Aldous_Broder
from MDP_state import convert_to_MDP
import re


def gamify_policy(policy):
    policy_string = '\n'.join([''.join(row) for row in policy])
    policy_string = re.sub('up', '↑', policy_string)
    policy_string = re.sub('down', '↓', policy_string)
    policy_string = re.sub('right', '→', policy_string)
    policy_string = re.sub('left', '←', policy_string)
    return policy_string


def policy_iteration(grid, gamma):

    policy_changed = True

    policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['up', 'down', 'left', 'right']

    iters = 0

    '''Policy iteration'''
    while policy_changed:
        policy_changed = False

        ''' 1- Policy evaluation '''
        # no transition probabilities = deterministic
        value_changed = True

        while value_changed:
            value_changed = False
            # Run value iteration for each state
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == '$':
                        policy[i][j] = '$'
                    else:
                        neighbor = getattr(grid[i][j], policy[i][j])
                        # V = R + γ Σ PV
                        v = grid[i][j].reward + gamma * grid[neighbor[0]][neighbor[1]].value
                        # Compare to previous iteration
                        if v != grid[i][j].value:
                            value_changed = True
                            grid[i][j].value = v

        '''2- Greedy Policy'''
        # Once values have converged for the policy, update policy with greedy approach
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != '$':
                    action_values = {a: grid[getattr(grid[i][j], a)[0]][getattr(grid[i][j], a)[1]].value for a in actions}
                    best_action = max(action_values, key=action_values.get)
                    # Compare to previous policy
                    if best_action != policy[i][j]:
                        policy_changed = True
                        policy[i][j] = best_action
        iters += 1

    return policy


if __name__ == '__main__':
    maze = Aldous_Broder(3, 3).generate()
    mdp = convert_to_MDP(maze)
    policy = policy_iteration(mdp, .9)
    policy_str = gamify_policy(policy)
    print(maze)
    print(policy_str)