import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 28)

# Colors
WHITE = (255, 255, 255)
BLUE = (66, 135, 245)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# Player setup
player = pygame.Rect(100, HEIGHT - 60, 40, 50)
player_vel_y = 0
GRAVITY = 0.8
JUMP_STRENGTH = -15
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 10, WIDTH, 10),
    pygame.Rect(200, 360, 120, 10),
    pygame.Rect(400, 300, 150, 10),
    pygame.Rect(100, 220, 100, 10),
    pygame.Rect(350, 150, 100, 10),
]

# Enemy setup
enemy = pygame.Rect(500, HEIGHT - 40, 40, 40)
enemy_dir = 1

# Coins
coins = [pygame.Rect(random.randint(100, 700), random.randint(100, 350), 20, 20) for _ in range(5)]
score = 0

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # Jumping
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = JUMP_STRENGTH
        on_ground = False

    # Gravity
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Collision with platforms
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:
            player.bottom = plat.top
            player_vel_y = 0
            on_ground = True

    # Keep player in screen
    if player.left < 0: player.left = 0
    if player.right > WIDTH: player.right = WIDTH

    # Enemy movement
    enemy.x += enemy_dir * 2
    if enemy.left <= 400 or enemy.right >= 750:
        enemy_dir *= -1

    # Collision with enemy
    if player.colliderect(enemy):
        screen.fill(RED)
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    # Coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    # Draw player
    pygame.draw.rect(screen, BLUE, player)

    # Draw enemy
    pygame.draw.rect(screen, RED, enemy)

    # Draw coins
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 10)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
