import pygame
import sys
import random

pygame.init()

width = 1300
height = 1000

red = (255, 0, 0)
blue = (0,0,255)
yellow = (255, 255, 0)
player_size = 50
player_position = [width/2, height - 2 * player_size]

background_color = (0, 0, 0)

enemy_size = 50
enemy_position = [random.randint(0, width - enemy_size), 0]
enemy_list = [enemy_position]

speed = 10

font = pygame.font.SysFont("monospace", 35)





screen = pygame.display.set_mode((width, height))

game_over = False

score = 0

clock = pygame.time.Clock()

def set_level(score, speed):
    if score < 20:
        speed = 6
    elif score < 40:
        speed = 9
    elif score < 60:
        speed = 12
    else:
        speed = 17
    return  speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])



def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, blue, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))


def update_enemy_pos(enemy_list, score):
    for idx, enemy_position in enumerate(enemy_list):

        if enemy_position[1] >= 0 and enemy_position[1] < height:
            enemy_position[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1

    return score
def collision_check(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_colsion(enemy_position, player_position):
            return  True
    return  False


def detect_colsion(player_position, enemy_postion):
    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_postion[0]
    e_y = enemy_postion[1]

    if e_x > p_x and e_x < (p_x + player_size) or p_x >= e_x and p_x < (e_x + enemy_size):
        if (e_y >= p_y and e_y <(p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return  True
    return  False



while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key ==  pygame.K_RIGHT:
                x += player_size

            player_position = [x, y]

    screen.fill(background_color)

    if detect_colsion(player_position, enemy_position):
        game_over = True
        break

    drop_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    speed = set_level(score, speed)
    text = "Score:" + str(score)
    label = font.render(text, 1, yellow)
    screen.blit(label, (width - 200, height - 40))

    if collision_check(enemy_list, player_position):
        game_over = True
        break
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, red, (player_position[0], player_position[1], player_size, player_size))

    pygame.display.update()

    clock.tick(30)