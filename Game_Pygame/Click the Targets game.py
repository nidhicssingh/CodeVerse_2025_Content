import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Targets")

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 24)
FPS = 60

# Game variables
score = 0
missed = 0
max_missed = 10
target_radius = 25
target_duration = 1500  # milliseconds

# Generate target as (x, y) center
def new_target():
    x = random.randint(target_radius, WIDTH - target_radius)
    y = random.randint(target_radius, HEIGHT - target_radius)
    return (x, y)

target_pos = new_target()
target_spawn_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx = mx - target_pos[0]
            dy = my - target_pos[1]
            if dx**2 + dy**2 <= target_radius**2:
                score += 1
                target_pos = new_target()
                target_spawn_time = current_time
            else:
                missed += 1

    # Timeout check
    if current_time - target_spawn_time > target_duration:
        missed += 1
        target_pos = new_target()
        target_spawn_time = current_time

    # Draw target
    pygame.draw.circle(screen, RED, target_pos, target_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    missed_text = font.render(f"Missed: {missed}/{max_missed}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))

    # Game over
    if missed >= max_missed:
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
