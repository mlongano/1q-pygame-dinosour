import pygame
from pygame.sprite import Sprite
from random import randint


class Mob(Sprite):

    def __init__(self):
        super().__init__()  # costruttore dello sprite

        snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
        snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()

        self.snail_frames = [snail_1, snail_2]

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.current_frame = 0

        # Modo piu' sintetico di creare i frame:
        # self.snail_frames = [
        #    pygame.image.load("graphics/snail/snail1.png").convert_alpha(),
        #    pygame.image.load("graphics/snail/snail2.png").convert_alpha(),
        # ]

        y_pos = 300

        self.image = snail_1
        self.rect = self.image.get_rect(bottomleft=(randint(900, 1100), y_pos))

    def update(self):
        self.rect.x -= 5
        self.animate()
        self.destroy_onexit()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.snail_frames)
            self.image = self.snail_frames[self.current_frame]

    # rimuovere lo sprite quando esce dallo schermo
    def destroy_onexit(self):
        if self.rect.right <= 0:
            self.kill()
