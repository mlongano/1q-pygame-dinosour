import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title
pygame.display.set_caption("Asteroid Dodger")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Load images
satellite_image = pygame.image.load("assets/images/satellite.png").convert_alpha()
satellite_image = pygame.transform.scale(satellite_image, (40, 40))
asteroid_image = pygame.image.load("assets/images/asteroid-1.png").convert_alpha()
asteroid_image = pygame.transform.scale(asteroid_image, (60, 60))
background_image = pygame.image.load("assets/images/space-background.png").convert()
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height)
)


class Satellite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = satellite_image
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height - 50))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player within bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = -self.rect.height  # Start offscreen
        self.speed = random.randrange(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = random.randrange(2, 5)


# Create sprite groups
all_sprites = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

# Create satellite
player = Satellite()
all_sprites.add(player)

# Game loop
running = True
clock = pygame.time.Clock()
asteroid_timer = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_timer, 1000)  # Spawn asteroids every second

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == asteroid_timer:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroid_group.add(asteroid)

    # Update
    all_sprites.update()

    # Collision detection
    if pygame.sprite.spritecollide(player, asteroid_group, True):
        # Game over - You'll need to handle this
        print("Game Over!")
        running = False

    # Draw / Render
    screen.blit(background_image, (0, 0))  # Optionali
    # screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
