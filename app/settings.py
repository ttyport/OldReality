import pygame
import json
import os
from common.learning_controls import KeySurface
from common.configmodel import Config

if os.path.exists("/usr/share/oldreality/"):
    resources_path = "/usr/share/oldreality/app/resources/"
else:
    resources_path = "resources/"


def reconfig():
    global lang, res, screen_width, screen_height, window, k, data

    configs = [
        Config('4K', 1600, 1400),
        Config('FullHD', 800, 700)
    ]
    with open(f"{str(os.path.expanduser('~'))}/.config/oldreality/config.txt", encoding="utf-8") as conf:
        conf = conf.read().split("\n")
        res = conf[0].split("=")[1]
        lang = conf[1].split("=")[1]
        for _config in configs:
            if res.lower() == _config.resolution_name:
                screen_width = _config.screen_width
                screen_height = _config.screen_height

    with open(f"{resources_path}langs/settings/{lang}.json", encoding="utf-8") as text:
        data = json.load(text)

    window = pygame.display.set_mode((screen_width, screen_height))
    k = 1600 / screen_width
    pygame.display.set_caption(data["title"])


def write_config():
    with open(f"{str(os.path.expanduser('~'))}/.config/oldreality/config.txt", "w", encoding="utf-8") as conf:
        print(f"Resolution={config[1]}", file=conf)
        print(f"Lang={config[0]}", file=conf)


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, x=None, left=False):
    size = size - 5 * (1 if int(k) == 2 else 2)
    font = pygame.font.Font(f'{resources_path}fonts/font.ttf', size)
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
    font = pygame.font.Font(f'{resources_path}fonts/font.ttf', size)
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


def draw_help():
    key_text_font = pygame.font.Font(f"{resources_path}fonts/font.ttf", int(60 // k))

    key_paddings = (30 // k, 20 // k)

    if not edited:
        enter_color = (0, 255, 0)
    else:
        enter_color = (255, 255, 0)

    arrow_left_text = KeySurface(key_text_font.render("←", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    arrow_right_text = KeySurface(key_text_font.render("→", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    arrow_up_text = KeySurface(key_text_font.render("↑", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    arrow_down_text = KeySurface(key_text_font.render("↓", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)
    enter_text = KeySurface(key_text_font.render("ENTER", True, enter_color), enter_color, (0, 0, 0),
                            key_paddings)
    escape_text = KeySurface(key_text_font.render("ESC", True, (0, 255, 0)), (0, 255, 0), (0, 0, 0), key_paddings)

    help_surface = pygame.Surface((screen_width, 300 / k))
    help_surface.blit(arrow_up_text, (5, 50 / k))
    help_surface.blit(arrow_down_text, (arrow_right_text.get_width() + 5, 50 / k))
    help_surface.blit(key_text_font.render(data["instructions"]["select"], True, (0, 255, 0)),
                      (arrow_right_text.get_width() * 2 + 50 / k, 70 / k))

    help_surface.blit(arrow_left_text, (5, 150 / k))
    help_surface.blit(arrow_right_text, (arrow_right_text.get_width() + 5, 150 / k))
    help_surface.blit(key_text_font.render(data["instructions"]["edit"], True, (0, 255, 0)),
                      (arrow_right_text.get_width() * 2 + 50 / k, 180 / k))

    help_surface.blit(enter_text, (arrow_right_text.get_width() * 2 + 550 / k, 50 / k))
    help_surface.blit(key_text_font.render(data["instructions"]["apply"], True, (0, 255, 0)),
                      (arrow_right_text.get_width() * 2 + enter_text.get_width() + 600 / k, 70 / k))

    help_surface.blit(escape_text, (arrow_right_text.get_width() * 2 + 550 / k, 150 / k))
    help_surface.blit(key_text_font.render(data["instructions"]["quit"], True, (0, 255, 0)),
                      (arrow_right_text.get_width() * 2 + escape_text.get_width() + 600 / k, 180 / k))

    window.blit(help_surface, (100 / k, screen_height - 300 / k))

    border = pygame.Rect(0, screen_height - 300 / k, screen_width, 300 / k)
    pygame.draw.rect(window, (0, 255, 0), border, 5, border_radius=5)


def main_menu():
    global x_coord, edited, startup_config
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
                    edited = True

                elif event.key == pygame.K_RIGHT:
                    coord = settings[x_coord].index(config[x_coord]) + 1
                    coord = coord if coord <= 1 else 0
                    config[x_coord] = settings[x_coord][coord]
                    edited = True

                elif event.key == pygame.K_RETURN:
                    write_config()
                    reconfig()
                    startup_config = config.copy()
                    edited = False

                elif event.key == pygame.K_ESCAPE:
                    import main
                    main.main()
            if config == startup_config:
                edited = False
        update_cursor()
        draw_list()
        draw_help()
        pygame.display.update()
    pygame.quit()


lang, res, data = None, None, None

pygame.init()
clock = pygame.time.Clock()

screen_width = 1600
screen_height = 1400

reconfig()

edited = False

k = 1600 / screen_width

settings_list = ["Language", "Resolution"]
config = [lang, res]
startup_config = config.copy()
language = ["en", "ru"]
resolution = ["4K", "FullHD"]
settings = [language, resolution]

x_coord = 0

window = pygame.display.set_mode((screen_width, screen_height))

main_menu()
