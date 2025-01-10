import math
import random
import time
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
LIVES = 30
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# Load and scale the background image
BACKGROUND_IMAGE = pygame.image.load("angry-bg.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Load the target images
TARGET_IMAGES = [
    pygame.image.load("minion-pig.png"),
    pygame.image.load("helmet-pig.png"),
    pygame.image.load("mustache-pig.png"),
    pygame.image.load("king-pig.png"),
]

class Target:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.original_size = 60
        self.max_size = 100
        self.min_size = 40
        self.size = self.original_size
        self.lifetime = 100  # Time the target stays active
        self.growth_rate = 0.5
        self.shrinking = False
    def update(self):
        if self.shrinking:
            self.size -= self.growth_rate
            if self.size <= self.min_size:
                self.shrinking = False
        else:
            self.size += self.growth_rate
            if self.size >= self.max_size:
                self.shrinking = True
        self.lifetime -= 1

        # Update the rectangle based on new size
        self.rect = pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
    def draw(self, win):
        scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        win.blit(scaled_image, (self.rect.x, self.rect.y))
    def collide(self, x, y):
        return self.rect.collidepoint(x, y)

def draw(win, targets):
    win.blit(BACKGROUND_IMAGE, (0, 0))
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill("black")
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                image = random.choice(TARGET_IMAGES)
                target = Target(x, y, image)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        for target in targets[:]:
            target.update()
            if target.lifetime <= 0:
                targets.remove(target)
                misses += 1
            elif click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()