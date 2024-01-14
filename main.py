import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 40, True)

COLOR_PLAYER = (72, 0, 151)
COLOR_DISPLAY = (1, 255, 255)
COLOR_ENEMIES = (255, 0, 0)
score_colors_list = ('yellow', 'green', 'purple', 'gold', 'pink', )
COLOR_SCORE = (random.choice(score_colors_list))

CREATE_ENEMY = pygame.USEREVENT +1 
CREATE_BONUS = pygame.USEREVENT +2
CHANGE_IMAGE = pygame.USEREVENT +3

pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 2500)
pygame.time.set_timer(CHANGE_IMAGE, 250)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('py-game/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "py-game/goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (10, 10)
player = pygame.image.load('py-game/player.png').convert_alpha()
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_up = [-0, -4]
player_move_right = [4, 0]
player_move_left = [-4, -0]
enemy_sizes = ((40, 20), (120, 60), (60, 30), (80, 40))

def create_enemy():
    enemy_size = (10, 10)
    enemy = pygame.transform.scale(pygame.image.load('py-game/enemy.png').convert_alpha(), (random.choice(enemy_sizes)))
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, 700), *enemy_size)
    enemy_move = [random.randint(-18, -6), random.randint(-2, 2)]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (10, 10)
    bonus = pygame.image.load('py-game/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(100, 1000), -30, *bonus_size)
    bonus_move = [random.randint(-3, 1), random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

playing = True
score = 0
enemies = []
bonus_list = []
player_image_index = 0

while playing:
    FPS.tick(220)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonus_list.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[player_image_index]))
            player_image_index += 1
        if player_image_index >= len(PLAYER_IMAGES):
            player_image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonus_list:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonus_list.pop(bonus_list.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_SCORE), (WIDTH -80, 30))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    
    for bonus in bonus_list:
        if bonus[1].bottom >= HEIGHT:
            bonus_list.pop(bonus_list.index(bonus))
    
     