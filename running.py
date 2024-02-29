import pygame
from random import randint, choice
from player import Player
from mob import Mob
from score import Score


# controlla se si sono verificate collisioni tra giocatore e mob
def collision_sprite() -> bool:
    # ritorna una lista degli sprite che collidono
    if pygame.sprite.spritecollide(player.sprite, mobs, False):
        return True

    return False


pygame.init()

w = 800
h = 400

# crea una finestra per il gioco
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Running game")

# timer del gioco
clock = pygame.time.Clock()

# controlla se sono in gioco o nei menu
game_active = True
score = Score()  # punteggio del gioco
lives = 5  # vite del giocatore
score_icon_pos = (10, 10)
lives_icon_pos = (100, 10)
# carico il font (e specifico la dimensione)
font = pygame.font.Font("fonts/Pixeltype.ttf", 50)

# Importa le icone
heart_icon = pygame.image.load("graphics/heart.png").convert_alpha()
heart_icon = pygame.transform.scale(heart_icon, (20, 20))
coin_icon = pygame.image.load("graphics/coins.png").convert_alpha()
coin_icon = pygame.transform.scale(coin_icon, (20, 20))

# carico gli sprite dello sfondo
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# main screen
# game_name = font.render()

# gestione degli sprite del giocatore
player = pygame.sprite.GroupSingle()
player.add(Player())  # istanza del giocatore aggiunta agli sprite

mobs = pygame.sprite.Group()
mobs.add(Mob(score))

# logica dello spawn (23 eventi base, i restanti sono per l'utente)
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1400)

# game cycle
run = True
while run:
    # gestione degli eventi
    for event in pygame.event.get():

        # controllo la chiusura della finestra
        if event.type == pygame.QUIT:
            run = False

        # controllo se è "scaduto" il timer e se il gioco è attivo
        if game_active and event.type == spawn_timer:
            mobs.add(Mob(score))

    # update del frame
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # disegno del punteggio
        # Blit delle icone
        screen.blit(coin_icon, score_icon_pos)
        for i in range(lives):
            screen.blit(
                heart_icon,
                (lives_icon_pos[0] + (i * heart_icon.get_width()), lives_icon_pos[1]),
            )

        # Visualizzazione del numero di punti
        score_text = font.render(str(score.get_value()), True, (255, 255, 255))
        screen.blit(
            score_text,
            (score_icon_pos[0] + coin_icon.get_width() + 5, score_icon_pos[1]),
        )

        player.draw(screen)
        player.update()

        mobs.draw(screen)
        mobs.update()

        for mob in mobs:
            if mob.rect.right <= 0:  # il mob è passato oltre il bordo sinistro
                mobs.remove(mob)
                score += 1
                mob.kill()  # rimuove il mob dalla lista

        if collision_sprite():
            lives -= 1
            mobs.empty()
            if lives == 0:
                game_active = False
    # game over
    else:
        screen.fill((94, 129, 162))

        # Create the "Game Over" text
        game_over_text = font.render("Game Over", True, (255, 255, 255))  # White text
        game_over_rect = game_over_text.get_rect(center=(w // 2, h // 2))

        # Draw the "Game Over" text on the screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(coin_icon, score_icon_pos)
        score_text = font.render(str(score.get_value()), True, (255, 255, 255))
        screen.blit(
            score_text,
            (score_icon_pos[0] + coin_icon.get_width() + 5, score_icon_pos[1]),
        )

    # disegno del prossimo frame
    pygame.display.update()

    # 60 fps
    clock.tick(60)

pygame.quit()
