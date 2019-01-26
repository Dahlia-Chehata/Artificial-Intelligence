import palette
import turtle
import random
from time import sleep
import maze_generator
import MDP_state
import time
import matplotlib.pyplot as plt
import numpy as np
from path_handling import *

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("square")
        self.color("#058c48")
        self.speed(0)
        self.ht()


def init_maze(state):
    screen.tracer(0, 0)
    for y in range(len(state)):
        for x in range(len(state[y])):
            character = state[y][x]
            screen_x = -130 + (x * 24)
            screen_y = 130 - (y * 24)
            # Check if barrier
            if character == "$":
                pen.goto(screen_x, screen_y)
                pen.stamp()
    # terminal state
    pen.color('red')
    pen.shape('circle')
    pen.goto(-106, 106)
    pen.stamp()
    screen.update()
    pen.color('red')
    pen.goto(-90, 170)
    pen.write('Iterations: 0', font=('Arial', 20, 'normal'))
    screen.update()
    pen.color('white')
    pen.goto(-90, -210)
    pen.write('Time : 0', font=('Arial', 15, 'normal'))
    screen.update()
    pen.goto(-90, -240)
    pen.write('Cost : 0', font=('Arial', 15, 'normal'))
    screen.update()



def value_iteration(grid, gamma):

    init_maze(grid)
    iters = 0
    tot_time = 0
    cost=0
    start_time = time.time()
    policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['up', 'down', 'left', 'right']
    sleep(1)

    value_changed = True
    while value_changed:
        value_changed = False
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != '$':
                    q = []
                    for a in actions:
                        neighbor = getattr(grid[i][j], a)
                        q.append(grid[i][j].reward + gamma * grid[neighbor[0]][neighbor[1]].value)
                    v = max(q)
                    cost = v #----------------> ??
                    if v != grid[i][j].value:
                        value_changed = True
                        grid[i][j].value = v

        iters += 1
        tot_time += time.time()-start_time
        visualize_values(grid, iters, tot_time, cost)
    turtle.done()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '$':
                action_values = {a: grid[getattr(grid[i][j], a)[0]][getattr(grid[i][j], a)[1]].value for a in actions}
                policy[i][j] = max(action_values, key=action_values.get)
            else:
                policy[i][j] = '$'

    return policy


def visualize_values(grid, iterations, time, cost):
    if cost != 0:
        for i in range(6):
            pen.undo()
    screen.tracer(0, 0)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            character = grid[y][x]

            screen_x = -130 + (x * 24)
            screen_y = 130 - (y * 24)

            pen.goto(screen_x, screen_y)

            if character == '$':
                pen.color('#058c48')
                pen.stamp()

            else:
                pen.color(gradient_dict.get(int(round(character.value / 5.) * 5), '#a89203'))
                pen.stamp()

    pen.color('red')
    pen.shape('circle')
    pen.goto(-106, 106)
    pen.stamp()

    pen.goto(-90, 170)
    pen.write('Iterations: {}'.format(iterations), font=('Arial', 20, 'normal'))
    screen.update()
    pen.color('white')
    pen.goto(-90, -210)
    pen.write('Time : ' + str(round(time, 5)), font=('Arial', 15, 'normal'))
    screen.update()
    pen.goto(-90, -240)
    pen.write('Cost : ' +  str(round(cost, 5)), font=('Arial', 15, 'normal'))
    screen.update()


if __name__ == '__main__':

    # initialize background
    screen = turtle.Screen()
    screen.bgcolor("Black")
    screen.title("Maze Game")
    screen.setup(500, 600)

    # turtle and gradient
    pen = Pen()
    gradient = palette.linear_gradient('#000000', '#a89203', 22)
    col_list = range(-10, 105, 5)
    gradient_dict = {col_list[i]: gradient.get('hex')[i] for i in range(len(gradient.get('hex')))}

    #maze
    random.seed(103)
    test = maze_generator.Aldous_Broder(5, 5).generate()
    test_mdp = MDP_state.convert_to_MDP(test)
    test_policy = value_iteration(test_mdp, .9)
    handle_path(test, test_policy, 9)

