import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Quiz Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Font
font = pygame.font.SysFont("comicsans", 28)
large_font = pygame.font.SysFont("comicsans", 40)

# Questions (format: [question, [choices], correct_index])
questions = [
    ["What is the capital of France?", ["Paris", "London", "Berlin", "Rome"], 0],
    ["Which planet is known as the Red Planet?", ["Earth", "Venus", "Mars", "Jupiter"], 2],
    ["What is the largest mammal?", ["Elephant", "Blue Whale", "Giraffe", "Shark"], 1],
    ["What is the square root of 64?", ["6", "8", "7", "9"], 1],
    ["Who wrote 'Hamlet'?", ["Shakespeare", "Hemingway", "Twain", "Dickens"], 0],
]

# Game variables
score = 0
question_index = 0
selected = None
feedback = ""
show_feedback = False
feedback_time = 0
timer_start = pygame.time.get_ticks()
QUESTION_TIME = 15000  # 15 seconds

# Button class
class Button:
    def __init__(self, rect, text, index):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.index = index

    def draw(self, surface):
        color = GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
def create_buttons(options):
    buttons = []
    for i, option in enumerate(options):
        btn = Button((100, 150 + i * 60, 500, 50), option, i)
        buttons.append(btn)
    return buttons

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Check if quiz is over
    if question_index >= len(questions):
        final_text = large_font.render(f"Quiz Over! Final Score: {score}/{len(questions)}", True, BLACK)
        screen.blit(final_text, (WIDTH // 2 - 250, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(4000)
        break

    # Get current question
    q_text, q_options, q_answer = questions[question_index]
    buttons = create_buttons(q_options)

    # Timer
    time_left = QUESTION_TIME - (pygame.time.get_ticks() - timer_start)
    if time_left <= 0:
        feedback = "⏰ Time's up!"
        show_feedback = True
        feedback_time = pygame.time.get_ticks()
        question_index += 1
        timer_start = pygame.time.get_ticks()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not show_feedback:
            pos = pygame.mouse.get_pos()
            for btn in buttons:
                if btn.is_clicked(pos):
                    selected = btn.index
                    if selected == q_answer:
                        feedback = "✅ Correct!"
                        score += 1
                    else:
                        feedback = f"❌ Wrong! Correct: {q_options[q_answer]}"
                    show_feedback = True
                    feedback_time = pygame.time.get_ticks()
                    question_index += 1
                    timer_start = pygame.time.get_ticks()
                    break

    # Draw question
    question_render = font.render(q_text, True, BLACK)
    screen.blit(question_render, (50, 50))

    # Draw buttons
    for btn in buttons:
        btn.draw(screen)

    # Draw timer
    time_text = font.render(f"Time left: {max(0, time_left // 1000)}s", True, RED if time_left < 5000 else BLACK)
    screen.blit(time_text, (500, 10))

    # Feedback display
    if show_feedback:
        fb_color = GREEN if "Correct" in feedback else RED
        fb_text = font.render(feedback, True, fb_color)
        screen.blit(fb_text, (50, 420))

        if pygame.time.get_ticks() - feedback_time > 2000:
            show_feedback = False
            selected = None

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
