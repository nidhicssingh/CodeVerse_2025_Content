import pygame
import requests
import time
import sys
from threading import Thread

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
GRID_POS = (50, 100)
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9
BUTTON_AREA_Y = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 24)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 240, 240)
BLACK = (0, 0, 0)
BLUE = (50, 100, 250)
GREEN = (20, 180, 50)
RED = (220, 30, 30)

# Fetch puzzle
def fetch_puzzle():
    try:
        response = requests.get("https://sugoku.onrender.com/board?difficulty=easy")
        return response.json()['board']
    except:
        return [[0]*9 for _ in range(9)]

# Globals
original_grid = fetch_puzzle()
grid = [row[:] for row in original_grid]
selected = None
start_time = time.time()

def draw_grid():
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (GRID_POS[0] + i*CELL_SIZE, GRID_POS[1]),
                         (GRID_POS[0] + i*CELL_SIZE, GRID_POS[1]+GRID_SIZE), thick)
        pygame.draw.line(screen, BLACK, (GRID_POS[0], GRID_POS[1] + i*CELL_SIZE),
                         (GRID_POS[0]+GRID_SIZE, GRID_POS[1]+i*CELL_SIZE), thick)

def draw_numbers():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color = BLACK if original_grid[i][j] != 0 else BLUE
                text = font.render(str(grid[i][j]), True, color)
                screen.blit(text, (GRID_POS[0] + j*CELL_SIZE + 20, GRID_POS[1] + i*CELL_SIZE + 10))

def draw_selection():
    if selected:
        pygame.draw.rect(screen, RED, (GRID_POS[0] + selected[1]*CELL_SIZE, GRID_POS[1] + selected[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def draw_buttons():
    buttons = ["Check", "Solve", "Hint", "Reset", "Exit"]
    for i, label in enumerate(buttons):
        pygame.draw.rect(screen, LIGHT_GRAY, (50 + i*105, BUTTON_AREA_Y, 100, 40), border_radius=5)
        text = small_font.render(label, True, BLACK)
        screen.blit(text, (50 + i*105 + 20, BUTTON_AREA_Y + 10))

def get_cell(pos):
    if GRID_POS[0] <= pos[0] < GRID_POS[0]+GRID_SIZE and GRID_POS[1] <= pos[1] < GRID_POS[1]+GRID_SIZE:
        return ((pos[1] - GRID_POS[1]) // CELL_SIZE, (pos[0] - GRID_POS[0]) // CELL_SIZE)
    return None

def is_valid(num, row, col):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    for i in range(3):
        for j in range(3):
            if grid[start_row+i][start_col+j] == num:
                return False
    return True

def solve_sudoku():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(num, i, j):
                        grid[i][j] = num
                        if solve_sudoku():
                            return True
                        grid[i][j] = 0
                return False
    return True

def give_hint():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(num, i, j):
                        grid[i][j] = num
                        return

def check_solution():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 or not is_valid(grid[i][j], i, j):
                return False
    return True

def draw_timer():
    elapsed = int(time.time() - start_time)
    minutes, seconds = divmod(elapsed, 60)
    time_text = small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
    screen.blit(time_text, (WIDTH - 150, 20))

# Main Loop
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    draw_selection()
    draw_buttons()
    draw_timer()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            selected = get_cell(pos)

            # Button clicks
            if BUTTON_AREA_Y <= pos[1] <= BUTTON_AREA_Y + 40:
                if 50 <= pos[0] < 150:
                    result = check_solution()
                    print("✅ Correct!" if result else "❌ Incorrect")
                elif 155 <= pos[0] < 255:
                    solve_sudoku()
                elif 260 <= pos[0] < 360:
                    give_hint()
                elif 365 <= pos[0] < 465:
                    grid = [row[:] for row in original_grid]
                elif 470 <= pos[0] < 570:
                    pygame.quit()
                    sys.exit()

        elif event.type == pygame.KEYDOWN and selected:
            row, col = selected
            if original_grid[row][col] == 0:
                if event.unicode.isdigit() and event.unicode != '0':
                    grid[row][col] = int(event.unicode)
                elif event.key == pygame.K_BACKSPACE:
                    grid[row][col] = 0

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
