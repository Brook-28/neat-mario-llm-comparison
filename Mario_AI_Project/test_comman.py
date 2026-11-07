from common import *

env = make_env()
state, info = env.reset()
print("inputs:", len(preprocess(state)), "(expected", NUM_INPUTS, ")")

steps = 0
done = False
while not done:
    action = ACTIONS.index(['right'])   # always run right
    state, reward, terminated, truncated, info = step_skip(env, action)
    steps += 1
    done = terminated or truncated

print("steps:", steps, "x reached:", info['x_pos'])
env.close()