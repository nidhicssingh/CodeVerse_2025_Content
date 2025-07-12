import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Font
font = pygame.font.SysFont("comicsans", 36)
big_font = pygame.font.SysFont("comicsans", 64)

# Game variables
word_list = ["apple", "banana", "keyboard", "python", "orange", "screen", "window", "speed", "type", "game"]
current_word = random.choice(word_list)
word_x = random.randint(50, WIDTH - 150)
word_y = 0
word_speed = 1.5

typed_text = ""
score = 0
lives = 3

clock = pygame.time.Clock()
FPS = 60

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw current word
    word_surface = font.render(current_word, True, BLUE)
    screen.blit(word_surface, (word_x, word_y))

    # Draw typed text
    typed_surface = font.render(f"Typed: {typed_text}", True, BLACK)
    screen.blit(typed_surface, (20, HEIGHT - 40))

    # Draw score and lives
    score_surface = font.render(f"Score: {score}", True, BLACK)
    lives_surface = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_surface, (20, 10))
    screen.blit(lives_surface, (WIDTH - 150, 10))

    pygame.display.flip()

    # Move word down
    word_y += word_speed

    # Word hit bottom
    if word_y > HEIGHT:
        lives -= 1
        typed_text = ""
        current_word = random.choice(word_list)
        word_x = random.randint(50, WIDTH - 150)
        word_y = 0
        if lives <= 0:
            running = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_text = typed_text[:-1]
            elif event.key == pygame.K_RETURN:
                # Submit attempt
                if typed_text == current_word:
                    score += 1
                    word_speed += 0.1  # Increase speed
                    current_word = random.choice(word_list)
                    word_x = random.randint(50, WIDTH - 150)
                    word_y = 0
                    typed_text = ""
                else:
                    typed_text = ""  # Reset on wrong enter
            else:
                typed_text += event.unicode

    clock.tick(FPS)

# Game Over Screen
screen.fill(WHITE)
game_over_text = big_font.render("Game Over!", True, RED)
final_score = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 60))
screen.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
sys.exit()
