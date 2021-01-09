import pygame
import random
import json
import os

from common.learning_controls import LearningControlsSurface, KeySurface
from common.configmodel import Config
from common.surface_combiner import Alignment, get_surfaces_into_column

configs = [
    Config('4k', 1610, 1400),
    Config('fullhd', 805, 700)
]

pygame.init()
clock = pygame.time.Clock()

screen_width = 1610
screen_height = 1400

with open(f"{str(os.path.expanduser('~'))}/.oldreality/config.txt", encoding="utf-8") as conf:
    conf = conf.read().split("\n")
    resolution = conf[0].split("=")[1].lower()
    lang = conf[1].split("=")[1].lower()
    for config in configs:
        if resolution == config.resolution_name:
            screen_width = config.screen_width
            screen_height = config.screen_height

with open(f"/usr/share/oldreality/app/resources/langs/arkanoid/{lang}.json", encoding="utf-8") as text:
    data = json.load(text)

k = 1610 // screen_width

play_height = 1198 / k
play_width = 1510 / k
player_width = 200 / k
player_height = 20 / k
ball_size = 30 / k
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 2

level = 1

v_x = random.choice((-10, 10))
v_y = -10
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
    for i in range(level + 2):
        for j in range(6):
            if level == 1:
                brick_types = [0]
            elif level == 2:
                brick_types = [0] * (i + 4) + [2] * (i + 1)
            elif level == 3:
                brick_types = [0] * (i + 2) + [2] * (i + 2) + [1] * (i // 2)

            bricks.append([pygame.Rect(j * (250 // k) + top_left_x + (5 // k),
                                       i * (50 // k) + top_left_y + (5 // k), 245 // k, 45 // k),
                           random.choice(brick_types)])
            if bricks[-1][1] == 0:
                bricks[-1].append((0, 255, 0))
            elif bricks[-1][1] == 1:
                bricks[-1].append((255, 0, 0))
            else:
                bricks[-1].append((255, 165, 0))
            if bricks[-1][1] == 2:
                bricks[-1].append(0)
    if level == 3:
        count = 0
        for el in bricks:
            if el[1] == 1:
                count += 1
        if count == 0:
            el = bricks[random.randint(0, len(bricks))]
            el[1] = 2
            bricks[-1] = (255, 0, 0)


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, left=False):
    font = pygame.font.Font('/usr/share/oldreality/app/resources/fonts/font.ttf', size)
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
    global v_x, v_y, time, lives, brick_types
    if lives <= 0:
        run = True
        while run:
            window.fill((0, 0, 0))

            font = pygame.font.Font('/usr/share/oldreality/app/resources/fonts/font.ttf', int(80 / k))
            game_over_texts = [font.render(data[key], True, (0, 255, 0)) for key in ("first_lose", "second", "third")]
            game_over_texts.insert(1, pygame.Surface((100, game_over_texts[0].get_height())))

            game_over_surface = get_surfaces_into_column(game_over_texts, Alignment.CENTER)
            game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            window.blit(game_over_surface, game_over_rect)

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


def check_empty_bricks():
    count_zero = 0
    for el in bricks:
        if el[1] in (0, 2):
            count_zero += 1

    return False if count_zero == 0 else True


def draw_bricks():
    global v_y, v_x, score, level, time, lives
    if check_empty_bricks() or level < 3:
        for el in bricks:
            pygame.draw.rect(window, el[2], el[0], border_radius=2)

        for elem in bricks:
            if ball.colliderect(elem[0]):
                el = elem[0]
                if abs(ball.right - el.left) < 30 / k:
                    v_x *= -1
                elif abs(ball.left - el.right) < 30 / k:
                    v_x *= -1
                elif abs(ball.bottom - el.top) < 30 / k and v_y > 0:
                    v_y *= -1
                elif abs(ball.top - el.bottom) < 30 / k and v_y < 0:
                    v_y *= -1

                if elem[1] == 0:
                    score += 5
                    bricks.remove(elem)
                elif elem[1] == 2:
                    if elem[-1] < 1:
                        elem[-1] += 1
                        elem[2] = (255, 255, 0)
                    else:
                        score += 10
                        bricks.remove(elem)

    else:
        run = True
        while run:
            window.fill((0, 0, 0))

            font = pygame.font.Font('/usr/share/oldreality/app/resources/fonts/font.ttf', int(80 / k))
            game_over_texts = [font.render(data[key], True, (0, 255, 0)) for key in ("first_won", "second", "third")]
            game_over_texts.insert(1, pygame.Surface((100, game_over_texts[0].get_height())))

            game_over_surface = get_surfaces_into_column(game_over_texts, Alignment.CENTER)
            game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            window.blit(game_over_surface, game_over_rect)

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
    global v_player, v_y, v_x, lives, level, time, score
    score = 0
    lives = 5
    init_objects()
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
            pygame.draw.rect(window, (0, 255, 0), ball)
            draw_text_middle(data["title"], int(100 / k), (0, 255, 0), window, delta_y=-450 / k)
            draw_text_middle(f"{data['score']}: {score}", int(75 / k), (0, 255, 0), window, delta_y=-450 / k,
                             delta_x=-screen_width / 3)
            draw_text_middle(f"{data['lives']}: {lives}", int(75 / k), (0, 255, 0), window, delta_y=-450 / k,
                             delta_x=screen_width / 3)
            pygame.display.update()
            clock.tick(int(60 / k))
        else:

            window.fill((0, 0, 0))
            main_menu_surface = get_instruction(data["paused"])
            main_menu_rect = main_menu_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            window.blit(main_menu_surface, main_menu_rect)
            pygame.display.update()
            paused = check_pause(paused)
            continue

        if not check_empty_bricks() and level < 3:
            level += 1
            lives = 5
            time = pygame.time.get_ticks()
            # Level up message 🤷
            draw_text_middle("Level Up!", int(100 // k), (0, 255, 0), window)
            restart()
            main_menu(True)

    pygame.quit()


def next_lvl():
    pass


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
    title_font = pygame.font.Font("/usr/share/oldreality/app/resources/fonts/font.ttf", 120 // k)
    key_text_font = pygame.font.Font("/usr/share/oldreality/app/resources/fonts/font.ttf", 60 // k)

    key_paddings = (30//k, 20//k)
    title_indent = 20//k

    arrow_left_text = KeySurface(key_text_font.render("←", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    arrow_right_text = KeySurface(key_text_font.render("→", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    space_text = KeySurface(key_text_font.render(data["space"].upper(), True, (0, 255, 0)), (0, 255, 0), (0, 0, 0),
                            key_paddings)
    escape_text = KeySurface(key_text_font.render("ESC", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)

    instructions = [
        {"keys": [arrow_left_text, arrow_right_text], "text": data["instructions"]["move_player"]},
        {"keys": [space_text], "text": data["instructions"]["pause"]},
        {"keys": [escape_text], "text": data["instructions"]["quit"]}
    ]

    main_menu_surface = LearningControlsSurface(title, (0, 255, 0), instructions, padding,
                                                title_indent, key_text_font, title_font)
    return main_menu_surface


def main_menu(launch=False):
    if not launch:
        run = True
        while run:
            window.fill((0, 0, 0))
            main_menu_surface = get_instruction(data["start_text"])
            main_menu_rect = main_menu_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            window.blit(main_menu_surface, main_menu_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main()
        pygame.quit()
    else:
        main()


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(data["title"])

main_menu()
