import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
COLOR_OPTIONS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 165, 0)   # Orange
]

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Memory Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 32)

# Create grid
tiles = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tiles.append(rect)

# Game variables
sequence = []
player_clicks = []
score = 0
showing_sequence = True
game_over = False
waiting_for_input = False

# Generate new sequence (4 unique positions + colors)
def generate_sequence():
    indices = random.sample(range(16), 4)
    seq = []
    for i in indices:
        color = random.choice(COLOR_OPTIONS)
        seq.append((i, color))
    return seq

# Show sequence step by step
def show_sequence(seq):
    for idx, color in seq:
        draw_grid()
        pygame.draw.rect(screen, color, tiles[idx])
        pygame.draw.rect(screen, BLACK, tiles[idx], 2)
        pygame.display.flip()
        pygame.time.delay(700)

        pygame.draw.rect(screen, GRAY, tiles[idx])
        pygame.draw.rect(screen, BLACK, tiles[idx], 2)
        pygame.display.flip()
        pygame.time.delay(300)

# Draw all tiles in default state
def draw_grid():
    screen.fill(WHITE)
    for tile in tiles:
        pygame.draw.rect(screen, GRAY, tile)
        pygame.draw.rect(screen, BLACK, tile, 2)

# Display UI
def draw_ui():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    instr = "Click the tiles in the correct order" if waiting_for_input else "Watch the sequence"
    info_text = font.render(instr, True, BLACK)
    screen.blit(info_text, (10, 50))

# Start the first sequence
sequence = generate_sequence()

# Game loop
running = True
while running:
    draw_grid()
    draw_ui()

    # Show the sequence if it's time
    if showing_sequence:
        pygame.time.delay(500)
        show_sequence(sequence)
        showing_sequence = False
        waiting_for_input = True
        player_clicks = []

    # Highlight tiles already clicked
    for i in player_clicks:
        pygame.draw.rect(screen, YELLOW, tiles[i])
        pygame.draw.rect(screen, BLACK, tiles[i], 2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and waiting_for_input and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for idx, tile in enumerate(tiles):
                if tile.collidepoint(mx, my):
                    player_clicks.append(idx)

                    # Check correctness
                    correct_idx = sequence[len(player_clicks) - 1][0]
                    if idx != correct_idx:
                        game_over = True
                        waiting_for_input = False
                    elif len(player_clicks) == len(sequence):
                        score += 1
                        pygame.time.delay(500)
                        sequence = generate_sequence()
                        showing_sequence = True
                        waiting_for_input = False
                    break

    if game_over:
        screen.fill(WHITE)
        draw_grid()
        game_text = font.render(f"Game Over! Score: {score}", True, BLACK)
        screen.blit(game_text, (WIDTH // 2 - 130, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    clock.tick(FPS)

pygame.quit()
sys.exit()
