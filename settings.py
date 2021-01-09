import pygame
import json
from common.learning_controls import LearningControlsSurface, KeySurface
from configmodel import Config


def reconfig():
    global lang, res, screen_width, screen_height, window, k, data
    configs = [
        Config('4K', 1600, 1400),
        Config('FullHD', 800, 700)
    ]
    with open("config.txt", encoding="utf-8") as conf:
        conf = conf.read().split("\n")
        res = conf[0].split("=")[1]
        lang = conf[1].split("=")[1]
        for _config in configs:
            if res.lower() == _config.resolution_name:
                screen_width = _config.screen_width
                screen_height = _config.screen_height

    with open(f"resources/langs/settings/{lang}.json", encoding="utf-8") as text:
        data = json.load(text)

    window = pygame.display.set_mode((screen_width, screen_height))
    k = 1600 / screen_width


def write_config():
    with open("config.txt", "w", encoding="utf-8") as conf:
        print(f"Resolution={config[1]}", file=conf)
        print(f"Lang={config[0]}", file=conf)


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, x=None, left=False):
    size = size - 5 * (1 if int(k) == 2 else 2)
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)
    _x = x if x else screen_width / 2
    if left:
        surface.blit(label, (_x + delta_x,
                                screen_height / 2 + delta_y))
    else:
        surface.blit(label, (_x - (label.get_width() / 2) + delta_x,
                                screen_height / 2 - label.get_height() * 2 + delta_y))


def label_size():
    size = int(100 / k)
    color = (0, 0, 0)
    text = f"{data[settings_list[x_coord]]} <{config[x_coord]}>"
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)
    return label.get_width()


def update_cursor():
    delta = label_size()
    draw_text_middle("<", int(100 / k), (0, 255, 0), window, x=delta + 200 / k,
                     delta_y=x_coord * 100 / k - (20 if int(k) == 1 else 10))


def draw_list():
    for i, el in enumerate(settings_list):
        el = data[el]
        draw_text_middle(f"{el} <{config[i]}>", int(100 / k), (0, 255, 0), window, delta_x=-600 / k,
                         delta_y=i * 100 / k - 200 / k, left=True)




def main_menu():
    global x_coord
    running = True
    while running:
        window.fill((0, 0, 0))
        draw_text_middle(data["title"], int(160 / k), (0, 255, 0), window, delta_y=-300 / k)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if x_coord < len(settings_list) - 1:
                        x_coord += 1
                    else:
                        x_coord = 0

                elif event.key == pygame.K_UP:
                    if x_coord > 0:
                        x_coord -= 1
                    else:
                        x_coord = len(settings_list) - 1

                elif event.key == pygame.K_LEFT:
                    coord = settings[x_coord].index(config[x_coord]) - 1
                    coord = coord if coord >= 0 else 1
                    config[x_coord] = settings[x_coord][coord]

                elif event.key == pygame.K_RIGHT:
                    coord = settings[x_coord].index(config[x_coord]) + 1
                    coord = coord if coord <= 1 else 0
                    write_config()
                    config[x_coord] = settings[x_coord][coord]

                elif event.key == pygame.K_RETURN:
                    write_config()
                    reconfig()

                elif event.key == pygame.K_ESCAPE:
                    import main
                    main.main()
        update_cursor()
        draw_list()
        pygame.display.update()
    pygame.quit()


lang, res, data = None, None, None

pygame.init()
clock = pygame.time.Clock()

screen_width = 1600
screen_height = 1400

reconfig()

k = 1600 / screen_width


settings_list = ["Language", "Resolution"]
config = [lang, res]
language = ["en", "ru"]
resolution = ["4K", "FullHD"]
settings = [language, resolution]


x_coord = 0

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(data["title"])

main_menu()