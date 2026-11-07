import csv
import os
import numpy as np
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace

# Fixed experiment settings
LEVEL = 'SuperMarioBros-1-1-v0'
ACTIONS = SIMPLE_MOVEMENT      # 7 actions
FRAME_SKIP = 4                 # each chosen action is held for 4 frames
MAX_GENERATIONS = 100          
STUCK_LIMIT = 80               # end episode if x_pos hasn't improved for this many steps


def make_env():
    env = gym_super_mario_bros.make(LEVEL)
    return JoypadSpace(env, ACTIONS)


def preprocess(state):
    # 240x256 RGB image -> 240 floats in 0..1 (15x16 grayscale grid)
    gray = state.mean(axis=2) / 255.0                       # (240, 256)
    small = gray.reshape(15, 16, 16, 16).mean(axis=(1, 3))  # (15, 16)
    return small.flatten().tolist()


NUM_INPUTS = 15 * 16
NUM_OUTPUTS = len(ACTIONS)


def step_skip(env, action):
    # Repeat one action for FRAME_SKIP frames. Returns the same tuple as env.step
    total_reward = 0
    for _ in range(FRAME_SKIP):
        state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        if terminated or truncated:
            break
    return state, total_reward, terminated, truncated, info


def log_generation(folder, generation, best, mean, elapsed):
    # Append one row per generation to <folder>/log.csv.
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, 'log.csv')
    new_file = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(['generation', 'best_fitness', 'mean_fitness', 'elapsed_seconds'])
        writer.writerow([generation, best, mean, round(elapsed, 2)])