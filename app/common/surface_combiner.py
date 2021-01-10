from enum import Enum
import pygame


class Alignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


def get_surfaces_into_column(surfaces, alignment=Alignment.LEFT, padding=0) \
        -> pygame.Surface:
    width = max(surf.get_width() for surf in surfaces)
    height = sum(surf.get_height() for surf in surfaces) + (len(surfaces) - 1) * padding
    surface = pygame.Surface((width, height))

    y = 0
    for game_over_text in surfaces:
        if alignment == Alignment.CENTER:
            game_over_rect = game_over_text.get_rect(centerx=width // 2, top=y)
        elif alignment == Alignment.LEFT:
            game_over_rect = game_over_text.get_rect(left=0, top=y)
        elif alignment == Alignment.RIGHT:
            game_over_rect = game_over_text.get_rect(right=width, top=y)
        else:
            game_over_rect = game_over_text.get_rect()

        surface.blit(game_over_text, game_over_rect)
        y += game_over_text.get_height() + padding

    return surface
