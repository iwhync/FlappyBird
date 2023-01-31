import pygame
import random
import sys
from time import sleep

# Initialize Pygame
pygame.init()

# Set window size
window_size = (400, 700)
screen_width = window_size[0]
screen_height = window_size[1]

# Create game window
screen = pygame.display.set_mode(window_size)

# Keep track of score
score = 0
score_font = pygame.font.Font(None, 50)
score_surf = score_font.render(str(score), 1, (0, 0, 0))
score_pos = [330, 10]

# Load bird image
bird_image = pygame.Surface((34, 24))
bird_image.fill((255, 0, 0))

# Load pipe image
pipe_image = pygame.Surface((52, 400))
pipe_image.fill((0, 255, 0))

# Set clock
clock = pygame.time.Clock()

# Set game variables
pipe_velocity = -4
game_over = False
pipe_gap = 220
bird_acceleration = 0.01
gravity = 0.5

# Bird class
class Bird:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 0
        self.acceleration = 0
        self.rect = image.get_rect(center=(x, y))

    def move(self):
        self.velocity += self.acceleration
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def jump(self):
        self.velocity = -9

    def hit_pipe(self, pipe):
        #making the hitbox just a bit more forgiving
            hitbox_width = self.rect.width * 0.5
            hitbox_height = self.rect.height * 0.5
            hitbox_x = self.rect.x + (self.rect.width - hitbox_width)
            hitbox_y = self.rect.y + (self.rect.height - hitbox_height)
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
            return hitbox_rect.colliderect(pipe.rect)

# Pipe class
class Pipe:
    def __init__(self, x, y, image, velocity):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = velocity
        self.rect = image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.x += self.velocity
        self.rect.x = self.x

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Create bird object
bird = Bird(100, 350, bird_image)

# Create pipes list
pipes = []

# Add initial pipes to pipes list
gap_y = random.randint(200, 500)
bottom_pipe = Pipe(screen_width, gap_y - pipe_image.get_height(), pipe_image, pipe_velocity)
top_pipe = Pipe(screen_width, gap_y + pipe_gap, pipe_image, pipe_velocity)
pipes.append(bottom_pipe)
pipes.append(top_pipe)

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    bird.acceleration = gravity
    bird.move()

    for pipe in pipes:
        if pipe.x + pipe_image.get_width() < 0:
            pipes.remove(pipe)
        pipe.move()
        if bird.hit_pipe(pipe) or bird.y > screen_height:
            # render "DEAD" message
            dead_surf = score_font.render("DEAD", 1, (255, 0, 0))
            screen.blit(dead_surf, (screen_width // 2 - dead_surf.get_width() // 2, screen_height // 2 - dead_surf.get_height() // 2))
            pygame.display.update()

            # wait for 1 second
            sleep(1)

            # restart the game
            score = 0
            score_surf = score_font.render(str(score), 1, (0, 0, 0))
            pipes = []
            gap_y = random.randint(200, 500)
            bottom_pipe = Pipe(screen_width, gap_y - pipe_image.get_height(), pipe_image, pipe_velocity)
            top_pipe = Pipe(screen_width, gap_y + pipe_gap, pipe_image, pipe_velocity)
            pipes.append(bottom_pipe)
            pipes.append(top_pipe)
            bird = Bird(100, 350, bird_image)
            break
    # Remove pipes that have gone off screen
    pipes = [pipe for pipe in pipes if pipe.x + pipe_image.get_width() > 0]

    # Add new pipes to the game if necessary
    if len(pipes) == 0 or pipes[-1].x <= screen_width - 200:
        gap_y = random.randint(100, 450)
        bottom_pipe = Pipe(screen_width, gap_y - pipe_image.get_height(), pipe_image, pipe_velocity)
        top_pipe = Pipe(screen_width, gap_y + pipe_gap, pipe_image, pipe_velocity)
        pipes.append(bottom_pipe)
        pipes.append(top_pipe)
        score += 1
        score_surf = score_font.render(str(score), 1, (0, 0, 0))

    screen.fill((255, 255, 255))

    for pipe in pipes:
        pipe.draw()

    bird.draw()
    
    screen.blit(score_surf, score_pos)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
