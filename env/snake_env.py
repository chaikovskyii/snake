import gym
from gym import spaces
import numpy as np

from .core.world import World
from .utils.renderer import Renderer
from settings.constants import SIZE



class SnakeEnv(gym.Env):
    metadata = {
        'render': ['human', 'rgb_array'],
        'observation.types': ['raw', 'rgb']
    }

    def __init__(self, size=SIZE, render_zoom=20, custom=False, start_position=None, start_direction_index=None,
                 food_position=None):
        self.custom = custom
        self.start_position = start_position
        self.start_direction_index = start_direction_index
        self.food_position = food_position
        self.SIZE = size
        self.world = World(self.SIZE, self.custom, self.start_position, self.start_direction_index, self.food_position)
        self.current_step = 0
        self.alive = True
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(self.SIZE[0], self.SIZE[1]),
                                            dtype=np.uint8)
        # Action space
        self.action_space = spaces.Discrete(len(self.world.DIRECTIONS))
        #  Set renderer
        self.RENDER_ZOOM = render_zoom
        self.renderer = None

    def step(self, action):
        reward, done, snake = self.world.move_snake(action)
        return self.world.get_observation(), reward, done, snake

    def render(self, mode='human', close=False):
        if not close:
            if self.renderer is None:
                self.renderer = Renderer(size=self.SIZE, zoom_factor=self.RENDER_ZOOM)
            return self.renderer.render(self.world.get_observation(), mode=mode, close=False)

    def close(self):
        if self.renderer:
            self.renderer.close()
            self.renderer = None