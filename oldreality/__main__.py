import pygame
import importlib
import sys
import os

from oldreality.configmodel import Config


configs = [
    Config('4k', 1600, 1400),
    Config('fullhd', 800, 700)
]

pygame.init()
clock = pygame.time.Clock()

screen_width = 1600
screen_height = 1400

with open("config.txt") as conf:
    conf = conf.read().split("\n")
    resolution = conf[0].split("=")[1].lower()

    for config in configs:
        if resolution == config.resolution_name:
            screen_width = config.screen_width
            screen_height = config.screen_height


k = 1600 / screen_width



games_list = ["tetris", "pong", "arkanoid"]
image_list = []

x_coord = 0


def load_image(name, colorkey=None):
    fullname = f"resources/images/{name}"
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


for el in games_list:
    image_list.append(load_image(el + ".png"))


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, left=False):
    size = size - 5 * (1 if int(k) == 2 else 2)
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)
    if left:
        surface.blit(label, (screen_width / 2 + delta_x,
                             screen_height / 2 + delta_y))
    else:
        surface.blit(label, (screen_width / 2 - (label.get_width() / 2) + delta_x,
                            screen_height / 2 - label.get_height() * 2 + delta_y))


def update_cursor():
    draw_text_middle(">", int(100 / k), (0, 255, 0), window, delta_x=int(300 / k),
                     delta_y=x_coord * 100 / k - (15 if int(k) == 1 else 10))
    window.blit(pygame.transform.scale(image_list[x_coord], (int(800 / k), int(800 / k))), (200 / k, 400 / k))
    border = pygame.Rect(200 / k, 400 / k, 800 / k, 800 / k)
    pygame.draw.rect(window, (0, 255, 0), border, 5)


def draw_list():
    for i, el in enumerate(games_list):
        draw_text_middle(el, int(100 / k), (0, 255, 0), window, delta_x=400 / k,
                         delta_y=i * 100 / k - 200 / k, left=True)


def main():
    global x_coord
    running = True
    while running:
        window.fill((0, 0, 0))
        draw_text_middle("OldReality", int(160 / k), (0, 255, 0), window, delta_y=-300 / k)
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
                    game = importlib.import_module(games_list[x_coord])
                    game.main_menu()
        update_cursor()
        draw_list()
        pygame.display.update()
    pygame.quit()


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Main game menu')

main()
