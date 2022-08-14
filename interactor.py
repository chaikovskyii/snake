import random, time

from pyglet.window.key import MOTION_UP, MOTION_DOWN, MOTION_LEFT, MOTION_RIGHT
from env.snake_env import SnakeEnv


def interact():
    env = SnakeEnv()
    done = False
    r = 0
    action = random.randrange(4)
    delay_time = 0.2
    env.render(mode='human')
    @env.renderer.viewer.window.event
    def on_text_motion(motion):
        nonlocal action
        if motion == MOTION_UP:
            action = 0
        elif motion == MOTION_DOWN:
            action = 2
        elif motion == MOTION_LEFT:
            action = 3
        elif motion == MOTION_RIGHT:
            action = 1

    while not done:
        time.sleep(delay_time)
        obs, reward, done, info = env.step(action)
        env.render(mode='human')
        if reward:
            r += reward
            delay_time -= 1/6 * delay_time

    return r


if __name__ == '__main__':
    interact()
