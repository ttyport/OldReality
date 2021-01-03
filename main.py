import pygame
import importlib
import sys
import os

pygame.init()

screen_width = 800
screen_height = 700

games_list = ["tetris", "pong"]
image_list = []

# pkg = importlib.import_module(games_list[0])

x_coord = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


for el in games_list:
    image_list.append(load_image(el + ".png"))


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0, left=False):
    font = pygame.font.Font('resources/font.ttf', size)
    label = font.render(text, True, color)
    if left:
        surface.blit(label, (screen_width / 2 + delta_x,
                             screen_height / 2 + delta_y))
    else:
        surface.blit(label, (screen_width / 2 - (label.get_width() / 2) + delta_x,
                            screen_height / 2 - label.get_height() * 2 + delta_y))


def update_cursor():
    draw_text_middle(">", 50, (0, 255, 0), screen, delta_x=150, delta_y=x_coord * 50)
    screen.blit(image_list[x_coord], (100, 200))
    border = pygame.Rect(100, 200, 400, 400)
    pygame.draw.rect(screen, (0, 255, 0), border, 5)



def draw_list():
    for i, el in enumerate(games_list):
        draw_text_middle(el, 50, (0, 255, 0), screen, delta_x=200, delta_y=i * 50 - 100, left=True)


def main():
    global x_coord
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text_middle("OldReality", 80, (0, 255, 0), screen, delta_y=-150)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    for el in games_list:
                        import tetris
                elif event.key == pygame.K_p:
                    import pong
                elif event.key == pygame.K_DOWN:
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
        update_cursor()
        draw_list()
        pygame.display.update()
    pygame.quit()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Main game menu')

main()