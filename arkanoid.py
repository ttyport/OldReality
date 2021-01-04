import pygame
import random
import importlib

pygame.init()
clock = pygame.time.Clock()

screen_width = 1610
screen_height = 1400

with open("config.txt") as conf:
    conf = conf.read().split("\n")
    resolution = conf[0].split("=")[1]
    if resolution == "4K":
        screen_width, screen_height = 1610, 1400
    elif resolution == "FullHD":
        screen_width, screen_height = 805, 700
    elif resolution == "small":
        screen_width, screen_height = 400, 350

k = 1610 / screen_width

play_height = 1198 / k
play_width = 1510 / k
player_width = 200 / k
player_height = 20 / k
ball_size = 30 / k
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 2

border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)
player = pygame.Rect(screen_width / 2 - player_width / 2, screen_height - player_height - 20,
                     player_width, player_height)
ball = pygame.Rect(player.center[0], player.top - ball_size,
                   ball_size, ball_size)

v_x = random.choice((-10, 10))
v_y = 10
v_player = 0

time = True

bricks = []


def init_bricks():
    global bricks
    for i in range(3):
        for j in range(6):
            bricks.append(pygame.Rect(j * (250 // k) + top_left_x + (10 // k), i * (50 // k) + top_left_y + (10 // k), 240 // k, 40 // k))


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, left=False):
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)
    if left:
        surface.blit(label, (screen_width / 2 + delta_x,
                             screen_height / 2 + delta_y))
    else:
        surface.blit(label, (screen_width / 2 - (label.get_width() / 2) + delta_x,
                            screen_height / 2 - label.get_height() * 2 + delta_y))


def draw_player():
    player.x += v_player
    if player.x <= top_left_x:
        player.x = top_left_x
    elif player.x > play_width - top_left_x * 3:
        player.x = play_width - top_left_x * 3


def restart():
    global v_x, v_y, time
    player.x, player.y = screen_width / 2 - player_width / 2, screen_height - player_height - 20
    ball.x, ball.y = player.center[0] - ball_size / 2, player.top - ball_size

    current_time = pygame.time.get_ticks()

    if current_time - time < 2100:
        v_x, v_y = 0, 0
    else:
        v_x, v_y = random.choice((-10, 10)), 10
        time = None


def draw_ball():
    global v_x, v_y, time
    ball.x += v_x
    ball.y += v_y

    if ball.left <= top_left_x:
        v_x *= -1
    elif ball.right > play_width + top_left_x:
        v_x *= -1
    elif ball.top < top_left_y:
        v_y *= -1

    if ball.colliderect(player):
        v_y *= -1

    if ball.bottom > screen_height:
        time = pygame.time.get_ticks()


def draw_bricks():
    global v_y, v_x
    for el in bricks:
        pygame.draw.rect(window, (0, 255, 0), el, border_radius=2)

    for el in bricks:
        if ball.colliderect(el):
            if abs(ball.right - el.left) < 10:
                v_x *= -1
            elif abs(ball.left - el.right) < 10:
                v_x *= -1
            elif abs(ball.bottom - el.top) < 10 and v_y > 0:
                v_y *= -1
            elif abs(ball.top - el.bottom) < 10 and v_y < 0:
                v_y *= -1
            bricks.remove(el)


def main():
    global v_player, v_y, v_x
    init_bricks()
    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    v_player -= 10
                elif event.key == pygame.K_LEFT:
                    v_player += 10
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    v_player += 10
                elif event.key == pygame.K_LEFT:
                    v_player -= 10
                if event.key == pygame.K_ESCAPE:
                    import main
                    main.main()
        draw_player()
        draw_ball()
        draw_bricks()
        if time:
            restart()

        pygame.draw.rect(window, (0, 255, 0), border, 5)
        pygame.draw.rect(window, (0, 255, 0), player, border_radius=5)
        pygame.draw.rect(window, (0, 255, 0), ball, border_radius=int(ball_size / 2))
        draw_text_middle("Arkanoid", int(100 / 2), (0, 255, 0), window, delta_y=-450 / k)
        pygame.display.update()
        clock.tick(int(60 / k))
    pygame.quit()


def main_menu():
    run = True
    while run:
        window.fill((0, 0, 0))

        draw_text_middle('Тест', int(120 / k), (0, 255, 0), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arkanoid')

main_menu()
