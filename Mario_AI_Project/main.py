import pygame
import numpy as np
import gym_super_mario_bros
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT
from nes_py.wrappers import JoypadSpace

env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
env = JoypadSpace(env, COMPLEX_MOVEMENT)
state, info = env.reset()

SCALE = 3
pygame.init()
window = pygame.display.set_mode((256 * SCALE + 16 * 20, 240 * SCALE))
pygame.display.set_caption("Super Mario Bros")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def choose_action(keys):
    buttons = set()
    if keys[pygame.K_d]:
        buttons.add('right')
    if keys[pygame.K_a]:
        buttons.add('left')
    if keys[pygame.K_s]:
        buttons.add('down')
    if keys[pygame.K_w]:
        buttons.add('A')
    if keys[pygame.K_LSHIFT]:
        buttons.add('B')
    for index, combo in enumerate(COMPLEX_MOVEMENT):
        if set(combo) == buttons:
            return index
    
    return 0


run_start_time = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = choose_action(pygame.key.get_pressed())
    state, reward, terminated, truncated, info = env.step(action)

    # Render the game screen
    picture = pygame.surfarray.make_surface(state.swapaxes(0, 1))
    picture = pygame.transform.scale(picture, (256 * SCALE, 240 * SCALE))
    window.blit(picture, (0, 0))
    
        # Render the small 15x16 grid representation
    small = state.mean(axis=2) / 255.0
    small = small.reshape(15, 16, 16, 16).mean(axis=(1, 3))

    cell_size = 20
    grid_x = 256 * SCALE

    for row in range(15):   
        for col in range(16):
            shade = int(small[row, col] * 255)
            color = (shade, shade, shade)
            pygame.draw.rect(
                window,
                color,
                (grid_x + col * cell_size, row * cell_size, cell_size, cell_size)
                ) 

    elapsed_seconds = (pygame.time.get_ticks() - run_start_time) / 1000
    label = font.render(f"x = {info['x_pos']} Time: {elapsed_seconds:.2f}s", True, (255, 255, 255))
    window.blit(label, (10, 240 * SCALE - 40))
    pygame.display.flip()
    clock.tick(60)  

    

    if terminated or truncated:
        print(f"Run ended. Furthest point: x={info['x_pos_max']}, reached the flag: {info['flag_get']}, Time: {elapsed_seconds:.2f}s")
        state, info = env.reset()
        run_start_time = pygame.time.get_ticks()
    


env.close()
pygame.quit()
print("done")