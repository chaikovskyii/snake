import numpy as np
import random

from settings.constants import DIRECTIONS, SNAKE_SIZE, DEAD_REWARD, \
    MOVE_REWARD, EAT_REWARD, FOOD_BLOCK, WALL
from env.core.snake import Snake

class World(object):
    def __init__(self, size, custom, start_position, start_direction_index, food_position):
        self.custom = custom
        self.start_position = start_position
        self.start_direction_index = start_direction_index
        self.food_position = food_position
        self.DEAD_REWARD = DEAD_REWARD
        self.MOVE_REWARD = MOVE_REWARD
        self.EAT_REWARD = EAT_REWARD
        self.FOOD = FOOD_BLOCK
        self.WALL = WALL
        self.DIRECTIONS = DIRECTIONS
        self.size = size
        self.world = np.zeros(size)
        print(self.world)
        self.world[0] = self.WALL
        self.world[-1] = self.WALL
        self.world[:, 0] = self.WALL
        self.world[:, -1] = self.WALL
        self.available_food_positions = set(zip(*np.where(self.world == 0)))
        self.snake = self.init_snake()
        self.init_food()

    def init_snake(self):
        if not self.custom:
            start_position = (random.randint(SNAKE_SIZE, self.size[0] - SNAKE_SIZE), random.randint(SNAKE_SIZE, self.size[1] - SNAKE_SIZE))
            start_direction_index = random.randint(0, len(DIRECTIONS) - 1)
            new_snake = Snake(start_position, start_direction_index, SNAKE_SIZE)
        else:
            new_snake = Snake(self.start_position, self.start_direction_index, SNAKE_SIZE)
        return new_snake

    def init_food(self):
        snake = self.snake if self.snake.alive else None
        available_food_positions = set(zip(*np.where(self.world == 0)))
        for x in self.snake.blocks:
            if x in available_food_positions:
                available_food_positions.remove(x)
        if not self.custom:
            chosen_position = random.sample(available_food_positions, 1)[0]
        else:
            chosen_position = self.food_position
            try:
                available_food_positions.remove(chosen_position)
            except:
                if (self.food_position[0] - 1, self.food_position[1]) in available_food_positions:
                    chosen_position = (self.food_position[0] - 1, self.food_position[1])
                else:
                    chosen_position = (self.food_position[0] - 1, self.food_position[1] + 1)
                available_food_positions.remove(chosen_position)
        self.world[chosen_position[0], chosen_position[1]] = self.FOOD
        self.food_position = chosen_position

    def get_observation(self):
        obs = self.world.copy()
        snake = self.snake if self.snake.alive else None
        if snake:
            for block in snake.blocks:
                obs[block[0], block[1]] = snake.snake_block
            obs[snake.blocks[0][0], snake.blocks[0][1]] = snake.snake_block + 1
        return obs

    def move_snake(self, action):
        reward = 0
        new_food_needed = False
        if self.snake.alive:
            new_snake_head, old_snake_tail = self.snake.step(action)
            if self.world[new_snake_head] == self.WALL:
                self.snake.alive = False
            elif new_snake_head in (self.snake.blocks[1:]):
                self.snake.alive = False
            if self.world[new_snake_head] == self.FOOD:
                self.world[new_snake_head] = 0
                self.snake.blocks.append(old_snake_tail)
                new_food_needed = True
                reward = self.EAT_REWARD
            elif self.snake.alive:
                reward = self.MOVE_REWARD
        done = not self.snake.alive
        reward = reward if self.snake.alive else self.DEAD_REWARD
        if new_food_needed:
            self.init_food()
        return reward, done, self.snake.blocks