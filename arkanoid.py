import pygame
import random
import importlib
import json

from configmodel import Config

configs = [
    Config('4k', 1610, 1400),
    Config('fullhd', 805, 700)
]

pygame.init()
clock = pygame.time.Clock()

screen_width = 1610
screen_height = 1400

with open("config.txt", encoding="utf-8") as conf:
    conf = conf.read().split("\n")
    resolution = conf[0].split("=")[1].lower()
    lang = conf[1].split("=")[1].lower()
    for config in configs:
        if resolution == config.resolution_name:
            screen_width = config.screen_width
            screen_height = config.screen_height

with open(f"resources/langs/arkanoid/{lang}.json", encoding="utf-8") as text:
    data = json.load(text)

k = 1610 / screen_width

play_height = 1198 / k
play_width = 1510 / k
player_width = 200 / k
player_height = 20 / k
ball_size = 30 / k
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 2

v_x = random.choice((-10, 10))
v_y = 10
v_player = 0

time = None

bricks = []

border = None
player = None
ball = None

score = 0
lives = 5


def init_objects():
    global border, player, ball
    border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)
    player = pygame.Rect(screen_width / 2 - player_width / 2, screen_height - player_height - 20,
                         player_width, player_height)
    ball = pygame.Rect(player.center[0], player.top - ball_size,
                       ball_size, ball_size)


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
    if player.left <= border.left + 5:
        player.left = border.left + 5
    elif player.right >= border.right - 5:
        player.right = border.right - 5


def restart():
    global v_x, v_y, time, lives
    if lives <= 0:
        run = True
        while run:
            window.fill((0, 0, 0))
            draw_text_middle(data["first_lose"], int(80 / k), (0, 255, 0), window, delta_y=-60 / k)
            draw_text_middle(data["second"], int(80 / k), (0, 255, 0), window, delta_y=120 / k)
            draw_text_middle(data["third"], int(80 / k), (0, 255, 0), window, delta_y=180 / k)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main_menu()
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        quit()
        pygame.quit()
    else:
        ball.x, ball.y = player.center[0] - ball_size / 2, player.top - ball_size

        current_time = pygame.time.get_ticks()

        if current_time - time < 2100:
            v_x, v_y = 0, 0
        else:
            v_x, v_y = random.choice((-10, 10)), 10
            time = None


def draw_ball():
    global v_x, v_y, time, lives
    ball.x += v_x
    ball.y += v_y

    if ball.left <= border.left + 5:
        v_x *= -1
    elif ball.right >= border.right - 5:
        v_x *= -1
    elif ball.top <= border.top + 5:
        v_y *= -1
    if ball.colliderect(player):
        if abs(ball.right - player.left) < 15:
            v_x *= -1
        elif abs(ball.left - player.right) < 15:
            v_x *= -1
        elif abs(ball.bottom - player.top) < 15 and v_y > 0:
            v_y *= -1
        elif abs(ball.top - player.bottom) < 15 and v_y < 0:
            v_y *= -1

    if ball.bottom > border.bottom + 5:
        lives -= 1
        time = pygame.time.get_ticks()


def draw_bricks():
    global v_y, v_x, score
    if len(bricks) > 0:
        for el in bricks:
            pygame.draw.rect(window, (0, 255, 0), el, border_radius=2)

        for el in bricks:
            if ball.colliderect(el):
                score += 5
                if abs(ball.right - el.left) < 15:
                    v_x *= -1
                elif abs(ball.left - el.right) < 15:
                    v_x *= -1
                elif abs(ball.bottom - el.top) < 15 and v_y > 0:
                    v_y *= -1
                elif abs(ball.top - el.bottom) < 15 and v_y < 0:
                    v_y *= -1
                bricks.remove(el)
    else:
        run = True
        while run:
            window.fill((0, 0, 0))
            draw_text_middle(data["first_won"], int(80 / k), (0, 255, 0), window, delta_y=-60 / k)
            draw_text_middle(data["second"], int(80 / k), (0, 255, 0), window, delta_y=120 / k)
            draw_text_middle(data["third"], int(80 / k), (0, 255, 0), window, delta_y=180 / k)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main_menu()
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        quit()
        pygame.quit()


def main():
    init_objects()
    global v_player, v_y, v_x, lives
    init_bricks()
    paused = False
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
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:
            draw_player()
            draw_ball()
            draw_bricks()
            if time:
                restart()

            pygame.draw.rect(window, (0, 255, 0), border, 5)
            pygame.draw.rect(window, (0, 255, 0), player, border_radius=5)
            pygame.draw.rect(window, (0, 255, 0), ball, border_radius=int(ball_size / 2))
            draw_text_middle(data["title"], int(100 / k), (0, 255, 0), window, delta_y=-450 / k)
            draw_text_middle(f"{data['score']}: {score}", int(100 / k), (0, 255, 0), window, delta_y=-450 / k,
                             delta_x=-screen_width / 3)
            draw_text_middle(f"{data['lives']}: {lives}", int(100 / k), (0, 255, 0), window, delta_y=-450 / k,
                             delta_x=screen_width / 3)
            pygame.display.update()
            clock.tick(int(60 / k))
        else:
            window.fill((0, 0, 0))
            draw_text_middle(data["pause"], int(120 / k), (0, 255, 0), window)
            pygame.display.update()
            paused = check_pause(paused)
            continue
    pygame.quit()


def check_pause(paused):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    return paused


def main_menu():
    run = True
    while run:
        window.fill((0, 0, 0))

        draw_text_middle(data["start_text"], int(120 / k), (0, 255, 0), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(data["title"])

main_menu()
