import pygame
from pygame.sprite import Sprite


class Player(Sprite):  # ereditato

    # costruttore
    def __init__(self):
        super().__init__()
        self.player_frames = {
            "walk": [
                pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(),
                pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(),
            ],
            "jump": [
                pygame.image.load("graphics/player/jump.png").convert_alpha(),
                pygame.image.load("graphics/player/player_stand.png").convert_alpha(),
            ],
        }

        self.current_frames = self.player_frames["walk"]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200

        self.grounded = True  # Change this to False when the player is in the air

        self.image = self.current_frames[self.current_frame]

        # hitbox
        self.rect = self.image.get_rect(midbottom=(80, 300))

        # fisica del giocatore
        self.gravity = 0

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1  # ad ogni frame riduco la gravità
        self.rect.y += self.gravity

        # se non sta toccando per terra
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def update(self):
        self.input()
        self.apply_gravity()
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame]

        if self.rect.bottom < 300:
            self.current_frames = self.player_frames["jump"]
        else:
            self.current_frames = self.player_frames["walk"]
