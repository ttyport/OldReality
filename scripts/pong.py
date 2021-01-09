import pygame
import random
import json

from common.learning_controls import KeySurface, LearningControlsSurface
from scripts.configmodel import Config

configs = [
    Config('4k', 1600, 1400),
    Config('fullhd', 800, 700)
]

# Инициализация pygame
pygame.init()
clock = pygame.time.Clock()

# Глобальные переменные
screen_width = 1600
screen_height = 1400

with open("config.txt", encoding="utf-8") as conf:
    conf = conf.read().split("\n")
    resolution = conf[0].split("=")[1].lower()
    lang = conf[1].split("=")[1].lower()
    for config in configs:
        if resolution == config.resolution_name:
            screen_width = config.screen_width
            screen_height = config.screen_height

with open(f"resources/langs/pong/{lang}.json", encoding="utf-8") as text:
    data = json.load(text)

k = 1600 // screen_width

ball_size = 30 / k
play_height = 1198 / k
play_width = 1500 / k
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 2

platform_height = 140 / k
platform_width = 10 / k

# Рисование основных элементов окна
ball = pygame.Rect(play_width / 2 - ball_size / 2, play_height / 2 - ball_size / 2,
                   ball_size, ball_size)
opponent = pygame.Rect(play_width + 20 / k, play_height / 2 + 20 / k + top_left_x, platform_width, platform_height)
player = pygame.Rect(20 / k + top_left_x, play_height / 2 + 20 / k + top_left_x, platform_width, platform_height)
border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)

# Переменные цвета
bg_color = (0, 0, 0)
green = (0, 255, 0)

# Переменные скорости
v_x = 10
v_y = 10
v_player = 0
v_opponent = 7

# Время
time = True

# Счет
player_score = 0
opponent_score = 0

# Звук
bounce = pygame.mixer.Sound("resources/sounds/pong.ogg")
win = pygame.mixer.Sound("resources/sounds/score.ogg")


def ai():
    if ball.x > screen_width / 2:
        if opponent.top < ball.y:
            opponent.top += v_opponent
        elif opponent.bottom > ball.y:
            opponent.bottom -= v_opponent
        if opponent.top <= top_left_y:
            opponent.top = top_left_y
        elif opponent.bottom >= screen_height:
            opponent.bottom = screen_height


def restart():
    global v_x, v_y, time

    ball.center = (play_width / 2 + top_left_x, play_height / 2 + top_left_y)
    current_time = pygame.time.get_ticks()

    if current_time - time < 700:
        draw_text_middle("3", int(100 / k), (0, 255, 0), window, delta_x=100 / k, delta_y=150 / k)
        v_x, v_y = 0, 0
    elif current_time - time < 1400:
        draw_text_middle("2", int(100 / k), (0, 255, 0), window, delta_x=100 / k, delta_y=150 / k)
        v_x, v_y = 0, 0
    elif current_time - time < 2100:
        draw_text_middle("1", int(100 / k), (0, 255, 0), window, delta_x=100 / k, delta_y=150 / k)
        v_x, v_y = 0, 0
    else:
        v_x, v_y = random.choice((-10, 10)), 10
        time = None


def draw_ball():
    global v_x, v_y, time, opponent_score, player_score
    ball.x += v_x
    ball.y += v_y

    if ball.top <= top_left_y + 5 or ball.bottom >= play_height + top_left_y:
        v_y *= -1
        pygame.mixer.Sound.play(bounce)
    if ball.left <= top_left_x:
        opponent_score += 1
        time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(win)
    elif ball.right > top_left_x + play_width:
        player_score += 1
        time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(win)
    if ball.colliderect(opponent) and v_x > 0:
        pygame.mixer.Sound.play(bounce)
        v_x *= -1
    if ball.colliderect(player) and v_x < 0:
        pygame.mixer.Sound.play(bounce)
        v_x *= -1


def draw_player():
    player.y += v_player
    if player.top <= top_left_y:
        player.top = top_left_y
    if player.bottom >= screen_height:
        player.bottom = screen_height


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0):
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2) + delta_x,
                         top_left_y + play_height / 2 - label.get_height() * 2 + delta_y))


def main():
    global v_player
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    v_player += 10
                elif event.key == pygame.K_UP:
                    v_player -= 10
                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_ESCAPE:
                    import main
                    main.main()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    v_player -= 10
                elif event.key == pygame.K_UP:
                    v_player += 10
        if not paused:
            draw_ball()
            draw_player()
            ai()

            window.fill(bg_color)
            pygame.draw.rect(window, green, player)
            pygame.draw.rect(window, green, opponent)
            pygame.draw.aaline(window, green, (screen_width / 2, top_left_y), (screen_width / 2, screen_height))
            pygame.draw.rect(window, green, ball)
            pygame.draw.rect(window, green, border, 5)
        else:
            window.fill((0, 0, 0))
            main_menu_surface = get_instruction(data["paused"])
            main_menu_rect = main_menu_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            window.blit(main_menu_surface, main_menu_rect)
            pygame.display.update()
            paused = check_pause(paused)
            continue

        if time:
            restart()

        draw_text_middle(data["title"], int(100 / k), (0, 255, 0), window, delta_y=-550 / k)
        draw_text_middle(f"{player_score}:{opponent_score}", int(50 / k), (0, 255, 0), window, delta_y=-550 / k)
        pygame.display.flip()
        clock.tick(int(60 / k))


def check_pause(paused):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    return paused


def get_instruction(title: str, padding=60 // k) -> pygame.Surface:
    title_font = pygame.font.Font("resources/fonts/font.ttf", 120 // k)
    key_text_font = pygame.font.Font("resources/fonts/font.ttf", 60 // k)

    key_paddings = (30//k, 20//k)
    title_indent = 20//k

    arrow_up_text = KeySurface(key_text_font.render("↑", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    arrow_down_text = KeySurface(key_text_font.render("↓", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    space_text = KeySurface(key_text_font.render(data["space"].upper(), True, (0, 255, 0)), (0, 255, 0), (0, 0, 0),
                            key_paddings)
    escape_text = KeySurface(key_text_font.render("ESC", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)

    instructions = [
        {"keys": [arrow_up_text, arrow_down_text], "text": data["instructions"]["move_player"]},
        {"keys": [space_text], "text": data["instructions"]["pause"]},
        {"keys": [escape_text], "text": data["instructions"]["quit"]}
    ]

    main_menu_surface = LearningControlsSurface(title, (0, 255, 0), instructions, padding,
                                                title_indent, key_text_font, title_font)
    return main_menu_surface


def main_menu():
    run = True
    while run:
        window.fill((0, 0, 0))

        main_menu_surface = get_instruction(data["start_text"])
        main_menu_rect = main_menu_surface.get_rect(center=(screen_width//2, screen_height//2))
        window.blit(main_menu_surface, main_menu_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


# Объявление окна
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(data["title"])

main_menu()  # Запуск игры
