import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 60
ROWS, COLS = 8, 8
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 102, 204)
BOX_COLOR = (204, 102, 0)
TARGET_COLOR = (0, 200, 0)
WALL_COLOR = (100, 100, 100)

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban Puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 40)

# Map layout
level = [
    "########",
    "#......#",
    "#..B...#",
    "#..P.T.#",
    "#..B...#",
    "#..T...#",
    "#......#",
    "########"
]

# Game elements
walls = []
boxes = []
targets = []
player_pos = None

# Parse level layout
for y in range(ROWS):
    for x in range(COLS):
        cell = level[y][x]
        if cell == "#":
            walls.append((x, y))
        elif cell == "B":
            boxes.append((x, y))
        elif cell == "T":
            targets.append((x, y))
        elif cell == "P":
            player_pos = (x, y)

# Movement directions
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def draw_tile(color, pos):
    rect = pygame.Rect(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)


def move(dx, dy):
    global player_pos, boxes
    px, py = player_pos
    nx, ny = px + dx, py + dy

    if (nx, ny) in walls:
        return

    if (nx, ny) in boxes:
        nnx, nny = nx + dx, ny + dy
        if (nnx, nny) not in walls and (nnx, nny) not in boxes:
            boxes.remove((nx, ny))
            boxes.append((nnx, nny))
            player_pos = (nx, ny)
    else:
        player_pos = (nx, ny)


def check_win():
    return all(box in targets for box in boxes)


# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw grid background
    for x in range(COLS):
        for y in range(ROWS):
            draw_tile(GRAY, (x, y))

    # Draw game objects
    for wall in walls:
        draw_tile(WALL_COLOR, wall)
    for target in targets:
        draw_tile(TARGET_COLOR, target)
    for box in boxes:
        draw_tile(BOX_COLOR, box)
    draw_tile(PLAYER_COLOR, player_pos)

    if check_win():
        win_text = font.render("Level Complete!", True, BLACK)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not check_win():
            if event.key in DIRECTIONS:
                dx, dy = DIRECTIONS[event.key]
                move(dx, dy)

    clock.tick(FPS)

pygame.quit()
sys.exit()
