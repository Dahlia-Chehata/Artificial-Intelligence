import turtle
import random
import maze_generator
import MDP_state
from time import sleep


# Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#a89203")
        self.penup()
        self.home()
        self.speed(0)
        self.ht()


# Create pen instance
pen = Pen()


def animate_PI(grid, gamma):
    policy_changed = True
    setup_maze(grid)
    actions = ['up', 'down', 'left', 'right']
    policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '$':
                policy[i][j] = '$'

    iters = 0
    visualize_policy(policy, iters)
    sleep(1)

    '''Policy iteration'''
    while policy_changed:
        policy_changed = False

        '''1- Policy evaluation'''
        # no Transition probabilities = deterministic
        is_value_changed = True
        while is_value_changed:
            is_value_changed = False
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == '$':
                        policy[i][j] = '$'
                    else:
                        neighbor = getattr(grid[i][j], policy[i][j])
                        v = grid[i][j].reward + gamma * grid[neighbor[0]][neighbor[1]].value
                        # Compare to previous iteration
                        if v != grid[i][j].value:
                            is_value_changed = True
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
        visualize_policy(policy, iters)
    turtle.done()
    return policy


def setup_maze(state):
    pen.ht()
    screen.tracer(0, 0)
    for y in range(len(state)):
        for x in range(len(state[y])):
            character = state[y][x]
            screen_x = -130 + (x * 24)
            screen_y = 130 - (y * 24)
            if character == "$":
                pen.goto(screen_x, screen_y)
                pen.stamp()
    pen.color('red')
    pen.goto(-106, 106)
    pen.stamp()
    screen.update()


def visualize_policy(policy, iterations):
    pen.undo()
    pen.shape('arrow')
    pen.ht()
    screen.tracer(0, 0)

    for y in range(len(policy)):
        for x in range(len(policy[y])):

            character = policy[y][x]

            screen_x = -130 + (x * 24)
            screen_y = 130 - (y * 24)

            if character != '$':
                pen.goto(screen_x, screen_y)
                pen.color('black')
                pen.shape('square')
                pen.stamp()
                pen.color('white')
                pen.shape('arrow')

            if character == 'up':
                pen.setheading(90)
                pen.stamp()

            if character == 'down':
                pen.setheading(270)
                pen.stamp()

            if character == 'left':
                pen.setheading(180)
                pen.stamp()

            if character == 'right':
                pen.setheading(0)
                pen.stamp()
    # terminal square
    pen.color('red')
    pen.shape('circle')
    pen.goto(-106, 106)
    pen.stamp()

    #update squares
    pen.color('black')
    x = [-130, -110, -90, -70, -50,-30,-10]
    for i in x:
        pen.goto(i, -234)
        pen.stamp()

    # iterations value
    pen.color('red')
    pen.goto(-100, -250)
    pen.write('Iterations: {}'.format(iterations),font=('Arial', 20, 'normal'))
    screen.update()


if __name__ == '__main__':

    # Set up background
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Maze Solver")
    screen.setup(500, 600)
    screen.bgpic('bk.gif')

    # Set up the maze
    random.seed(105)
    test = maze_generator.Aldous_Broder(5, 5).generate()
    # test = [['$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$'],
    #         ['$', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$'],
    #         ['$', ' ', '$', '$', '$', '$', '$', '$', '$', '$', '$', ' ', '$'],
    #         ['$', ' ', '$', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$'],
    #         ['$', ' ', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$'],
    #         ['$', ' ', '$', ' ', ' ', ' ', '$', ' ', ' ', ' ', ' ', ' ', '$'],
    #         ['$', ' ', '$', ' ', '$', ' ', '$', ' ', '$', '$', '$', ' ', '$'],
    #         ['$', ' ', ' ', ' ', '$', ' ', '$', ' ', '$', ' ', ' ', ' ', '$'],
    #         ['$', ' ', '$', ' ', '$', '$', '$', ' ', '$', ' ', '$', '$', '$'],
    #         ['$', ' ', '$', ' ', ' ', ' ', '$', ' ', '$', ' ', '$', ' ', '$'],
    #         ['$', ' ', '$', '$', '$', ' ', '$', ' ', '$', ' ', '$', ' ', '$'],
    #         ['$', ' ', ' ', ' ', '$', ' ', ' ', ' ', '$', ' ', ' ', ' ', '$'],
    #         ['$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$']]
    test_mdp = MDP_state.convert_to_MDP(test)
    test_policy = animate_PI(test_mdp, .5)

