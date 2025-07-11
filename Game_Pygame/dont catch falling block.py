import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemies")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player setup
player_width = 60
player_height = 15
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 40
player_speed = 5

# Enemy setup
enemy_width = 30
enemy_height = 30
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont("comicsans", 24)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player with mouse
    mouse_x = pygame.mouse.get_pos()[0]
    player_x = mouse_x - player_width // 2

    # Keep player in bounds
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Move enemy
    enemy_y += enemy_speed

    # Reset enemy and increase score
    if enemy_y > HEIGHT:
        enemy_y = -enemy_height
        enemy_x = random.randint(0, WIDTH - enemy_width)
        score += 1

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

    if player_rect.colliderect(enemy_rect):
        print("Game Over! Final Score:", score)
        running = False

    # Draw player and enemy
    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, enemy_rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
