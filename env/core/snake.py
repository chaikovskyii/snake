import numpy as np

from settings.constants import DIRECTIONS, SNAKE_BLOCK


class Snake:
    def __init__(self, head_position, direction_index, length):
        self.snake_block = SNAKE_BLOCK
        self.current_direction_index = direction_index
        self.alive = True
        self.blocks = [head_position]
        current_position = np.array(head_position)
        for i in range(1, length):
            current_position = current_position - DIRECTIONS[self.current_direction_index]
            self.blocks.append(tuple(current_position))

    def step(self, action):
        if (self.current_direction_index != action) and (np.abs(self.current_direction_index - action) != 2):
            self.current_direction_index = action
        tail = self.blocks[-1]
        self.blocks = self.blocks[:-1]
        new_head = tuple(self.blocks[0] + DIRECTIONS[self.current_direction_index])
        self.blocks = [new_head] + self.blocks
        return new_head, tail