import random
import os
import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 40)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('img/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "img/goose/"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('img/player.png').convert_alpha()
player_rect = player.get_rect(midleft=(0, HEIGHT // 2))

player_move_down = [0, 4]
player_speed_right = [4, 0]
player_speed_left = [-4, 0]
player_speed_up = [0, -4]

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('img/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(int(0.15 * HEIGHT), int(0.85 * HEIGHT)), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.image.load('img/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(int(0.15 * WIDTH), int(0.85 * WIDTH)), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

bonusing = []
enemies = []

score = 0

image_index = 0

plaing = True
game_over = False

while plaing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            plaing = False
        if event.type == CREATE_ENEMY and not game_over:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS and not game_over:
            bonusing.append(create_bonus())
        if event.type == CHANGE_IMAGE and not game_over:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_speed_right)

        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_speed_left)

        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_speed_up)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                game_over = True
                game_over_text = FONT.render("Game over", True, COLOR_BLACK)
                main_display.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                break

        for bonus in bonusing:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                bonusing.pop(bonusing.index(bonus))

                if score >= 20:
                    game_over = True
                    win_text = FONT.render("Бантерогусь успішно долетів", True, COLOR_BLACK)
                    main_display.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                    break

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    if game_over:
        pygame.time.wait(3000)
        plaing = False

    enemies = [enemy for enemy in enemies if enemy[1].left >= 0]
    bonusing = [bonus for bonus in bonusing if bonus[1].bottom <= HEIGHT]
