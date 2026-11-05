import pygame
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace

env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)
state, info = env.reset()

SCALE = 3
pygame.init()
window = pygame.display.set_mode((256 * SCALE, 240 * SCALE))
pygame.display.set_caption("Super Mario Bros")
clock = pygame.time.Clock()

running = True
step = 0
while running and step < 600:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = env.action_space.sample()
    state, reward, terminated, truncated, info = env.step(action)

    # Render the game screen
    picture = pygame.surfarray.make_surface(state.swapaxes(0, 1))
    picture = pygame.transform.scale(picture, (256 * SCALE, 240 * SCALE))
    window.blit(picture, (0, 0))
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

    if step % 50 == 0:
        print(f"step {step:4d}   x={info['x_pos']:4d}   time={info['time']}   flag={info['flag_get']}")

    if terminated or truncated:
        print("run ended")
        state, info = env.reset()

    step += 1


env.close()
pygame.quit()
print("done")