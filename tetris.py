import pygame
import random

from configmodel import Config

configs = [
    Config('4k', 1600, 1400),
    Config('fullhd', 800, 700)
]
pygame.font.init()

# Глобальные переменные

screen_width = 800
screen_height = 700

try:
    with open("config.txt") as conf:
        conf = conf.read().split("\n")
        resolution = conf[0].split("=")[1].lower()
        for config in configs:
            if resolution == config.resolution_name:
                screen_width = config.screen_width
                screen_height = config.screen_height
except Exception as e:
    print(e)


k = 1600 / screen_width

play_width = 600 / k
play_height = 1200 / k
block_size = 60 / k

fps = 30 * k

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

# Фигурки

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # Число 0-3


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0):
    font = pygame.font.Font('resources/fonts/font.ttf', size)
    label = font.render(text, True, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2) + delta_x,
                         top_left_y + play_height / 2 - label.get_height() * 2 + delta_y))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))  # Горизонтальные линии
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))  # Вертикальные линии


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.Font('resources/fonts/font.ttf', int(60 / k))
    label = font.render('Next Shape', True, (0, 255, 0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size,
                                                        block_size, block_size))
                pygame.draw.rect(surface, (128, 128, 128), (sx + j * block_size, sy + i * block_size,
                                                            block_size, block_size), 1)

    surface.blit(label, (sx + 20 / k, sy - block_size))


def draw_window(surface):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.Font('resources/fonts/font.ttf', int(120 / k))
    label = font.render('TETRIS', True, (0, 255, 0))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), block_size))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    # Рисуем клетки и границы
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (0, 255, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    paused = False

    key_left_pressed_time = 0
    key_right_pressed_time = 0
    pressed_time_for_move = 12 * k

    fall_speed = 0.14

    while run:
        if not paused:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()

            # PIECE FALLING CODE
            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
        else:
            window.fill((0, 0, 0))
            draw_text_middle('Paused', int(120 / k), (0, 255, 0), window)
            pygame.display.update()
            paused = check_pause(paused)
            continue

        def moveShapeLeft():
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1

        def moveShapeRight():
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_LEFT:
                #     current_piece.x -= 1
                #     if not valid_space(current_piece, grid):
                #         current_piece.x += 1

                # if event.key == pygame.K_RIGHT:
                #     current_piece.x += 1
                #     if not valid_space(current_piece, grid):
                #         current_piece.x -= 1
                if event.key == pygame.K_LEFT:
                    moveShapeLeft()
                elif event.key == pygame.K_RIGHT:
                    moveShapeRight()

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_ESCAPE:
                    import main
                    main.main()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_left_pressed_time = 0
                elif event.key == pygame.K_RIGHT:
                    key_right_pressed_time = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            current_piece.y += 1 
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
        elif keys[pygame.K_LEFT]:
            key_left_pressed_time += 1
            if key_left_pressed_time >= pressed_time_for_move:
                moveShapeLeft()
        elif keys[pygame.K_RIGHT]:
            key_right_pressed_time += 1
            if key_right_pressed_time >= pressed_time_for_move:
                moveShapeRight()

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

            fall_speed -= 0.0005

        draw_window(window)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

        clock.tick(fps)

    window.fill((0, 0, 0))
    draw_text_middle("You Lost.", int(40 / k), (0, 255, 0), window, delta_y=-30)
    draw_text_middle("Press enter to restart,", int(40 / k), (0, 255, 0), window, delta_y=60)
    draw_text_middle("or esc to exit.",int(40 / k), (0, 255, 0), window, delta_y=90)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.display.quit()
                    quit()
                elif event.key == pygame.K_RETURN:
                    run = False
                    main_menu()



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

        draw_text_middle('Press any key to begin.', int(120 / k), (0, 255, 0), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

main_menu()  # Запуск игры
