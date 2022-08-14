import numpy as np

SIZE = (32, 32)
SNAKE_SIZE = 3

WALL = 255
FOOD_BLOCK = 64
SNAKE_BLOCK = 100
DIRECTIONS = [np.array([-1, 0]),
              np.array([0, 1]),
              np.array([1, 0]),
              np.array([0, -1])]
DEAD_REWARD = -1.0
MOVE_REWARD = 0.0
EAT_REWARD = 1.0