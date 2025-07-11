import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 24)

# Snake and food
snake = [(5, 5)]
direction = (1, 0)
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

def draw_cell(x, y, color):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    return [new_head] + snake[:-1]

def grow_snake(snake, direction):
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    return [new_head] + snake

def is_collision(pos, snake):
    x, y = pos
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or pos in snake

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Move snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if is_collision(new_head, snake):
        break  # Game Over

    if new_head == food:
        snake = grow_snake(snake, direction)
        score += 1
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in snake:
                break
    else:
        snake = move_snake(snake, direction)

    # Draw snake and food
    for segment in snake:
        draw_cell(segment[0], segment[1], GREEN)

    draw_cell(food[0], food[1], RED)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)

# Game Over screen
screen.fill(WHITE)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, RED)
screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 10))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
sys.exit()
