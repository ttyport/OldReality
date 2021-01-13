import pygame
import importlib
import sys
import os
import json

from common.configmodel import Config


if os.path.exists("/usr/share/oldreality/"):
    resources_path = "/usr/share/oldreality/app/resources/"
else:
    resources_path = "resources/"


def reconfig():
    global resources_path, configs, clock, screen_width, screen_height, resolution, data, k

    if not os.path.exists(f"{str(os.path.expanduser('~'))}/.config/oldreality/"):
        os.makedirs(f"{str(os.path.expanduser('~'))}/.config/oldreality/")
        make_config = open(f"{str(os.path.expanduser('~'))}/.config/oldreality/config.txt", "w+", encoding="utf-8")
        print("Resolution=FullHD\nLang=en", file=make_config)
        make_config.close()

    configs = [
        Config('4k', 1600, 1400),
        Config('fullhd', 800, 700)
    ]
    pygame.init()
    clock = pygame.time.Clock()

    screen_width = 1600
    screen_height = 1400

    with open(f"{str(os.path.expanduser('~'))}/.config/oldreality/config.txt", encoding="utf-8") as conf:
        conf = conf.read().split("\n")

    resolution = conf[0].split("=")[1].lower()
    lang = conf[1].split("=")[1].lower()

    for config in configs:
        if resolution == config.resolution_name:
            screen_width = config.screen_width
            screen_height = config.screen_height

    k = 1600 / screen_width

    with open(f"{resources_path}langs/main/{lang}.json", encoding="utf-8") as text:
        data = json.load(text)

    pygame.display.set_caption(data["title"])


games_list = ["tetris", "pong", "arkanoid", "settings", "quit"]
image_list = []

x_coord = 0


def load_image(name, colorkey=None):
    global resources_path
    fullname = f"{resources_path}images/{name}"
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


for i, el in enumerate(games_list):
    image_list.append(load_image(el + ".png") if i not in
                                                 [len(games_list) - 2, len(games_list) - 1] else None)


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, left=False):
    size = size - 5 * (1 if int(k) == 2 else 2)
    font = pygame.font.Font(f'{resources_path}fonts/font.ttf', size)
    label = font.render(text, True, color)
    if left:
        surface.blit(label, (screen_width / 2 + delta_x,
                             screen_height / 2 + delta_y))
    else:
        surface.blit(label, (screen_width / 2 - (label.get_width() / 2) + delta_x,
                             screen_height / 2 - label.get_height() * 2 + delta_y))


def update_cursor():
    draw_text_middle(">", int(100 / k), (0, 255, 0), window, delta_x=int(200 / k),
                     delta_y=x_coord * 100 / k - (15 if int(k) == 1 else 10))
    if image_list[x_coord] is not None:
        window.blit(pygame.transform.scale(image_list[x_coord], (int(800 / k), int(800 / k))), (100 / k, 400 / k))
        border = pygame.Rect(100 / k, 400 / k, 800 / k, 800 / k)
        pygame.draw.rect(window, (0, 255, 0), border, 5)


def draw_list():
    for i, el in enumerate(games_list):
        el = data[el]
        draw_text_middle(el, int(100 / k), (0, 255, 0), window, delta_x=300 / k,
                         delta_y=i * 100 / k - 200 / k, left=True)


def main():
    global x_coord
    reconfig()
    running = True
    while running:
        window.fill((0, 0, 0))
        draw_text_middle("OldReality", int(160 / k), (0, 255, 0), window, delta_y=-300 / k)
        draw_text_middle('author yayguy4618, GPLv3 license', int(40 // k), (0, 255, 0), window,
                         delta_y=(screen_height) // 2, delta_x=-(screen_width - 550 // k) // 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if x_coord < len(games_list) - 1:
                        x_coord += 1
                    else:
                        x_coord = 0

                elif event.key == pygame.K_UP:
                    if x_coord > 0:
                        x_coord -= 1
                    else:
                        x_coord = len(games_list) - 1
                elif event.key == pygame.K_RETURN:
                    if x_coord != len(games_list) - 1:
                        pygame.display.set_caption(data[games_list[x_coord]])
                        game = importlib.import_module(games_list[x_coord])
                        game.main_menu()
                    else:
                        running = False
                        quit()

        update_cursor()
        draw_list()
        pygame.display.update()
    pygame.quit()


k, configs, clock, screen_width, screen_height, resolution, data = \
    None, None, None, None, None, None, None

reconfig()

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(data["title"])

main()
