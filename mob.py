import pygame
from pygame.sprite import Sprite
from random import randint
from score import Score


class Mob(Sprite):

    def __init__(self, mob_type, score: Score):
        super().__init__()  # costruttore dello sprite

        self.mob_frames = {
            "snail": [
                pygame.image.load("graphics/snail/snail1.png").convert_alpha(),
                pygame.image.load("graphics/snail/snail2.png").convert_alpha(),
            ],
            "fly": [
                pygame.image.load("graphics/fly/fly1.png").convert_alpha(),
                pygame.image.load("graphics/fly/fly2.png").convert_alpha(),
            ],
        }

        self.last_update = pygame.time.get_ticks()
        self.current_frames = self.mob_frames[mob_type]
        self.current_frame = 0
        self.frame_rate = 100

        y_pos = 300

        self.image = self.current_frames[self.current_frame]
        self.rect = self.image.get_rect(bottomleft=(randint(900, 1100), y_pos))

        self.score = score

    def update(self):
        self.rect.x -= 5
        self.animate()
        self.destroy()

    # rimuovere lo sprite quando esce dallo schermo
    def destroy(self):
        if self.rect.right <= 0:
            self.score.increment()
            self.kill()
