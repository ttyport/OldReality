import pygame
from typing import List, Tuple
from scripts.common import Alignment, get_surfaces_into_column


class KeySurface(pygame.Surface):
    def __init__(self,
                 text_surface: pygame.Surface,
                 color: Tuple[int, int, int],
                 bg_color: Tuple[int, int, int],
                 paddings: Tuple[int, int],
                 border=2,
                 border_radius=5):
        width = paddings[0]*2 + text_surface.get_width()
        height = paddings[1]*2 + text_surface.get_height()

        super().__init__((width, height))

        super().fill(bg_color)
        pygame.draw.rect(self, color, super().get_rect(), width=border, border_radius=border_radius)

        text_rect = text_surface.get_rect(center=(width//2, height//2))
        super().blit(text_surface, text_rect)


class InstructionSurface(pygame.Surface):
    def __init__(self,
                 keys: List[KeySurface],
                 text_surface: pygame.Surface,
                 indent_text: int):
        keys_width = sum(key.get_width() for key in keys)
        width = keys_width + indent_text + text_surface.get_width()
        height = max(key.get_height() for key in keys)

        super().__init__((width, height))
        x = 0
        for key in keys:
            key_rect = key.get_rect(left=x)
            super().blit(key, key_rect)
            x += key_rect.width

        x += indent_text

        text_rect = text_surface.get_rect(left=x, centery=height//2)
        super().blit(text_surface, text_rect)


def _get_instruction_surfaces(instructions, font: pygame.font.Font, color, padding: int):
    instruction_surfaces = []
    for el in instructions:
        keys, instruction_text = el["keys"], el["text"]
        text_surface = font.render(instruction_text, True, color)
        instruction_surface = InstructionSurface(keys, text_surface, padding)
        instruction_surfaces.append(instruction_surface)
    return instruction_surfaces


class LearningControlsSurface(pygame.Surface):
    def __init__(self,
                 title: str,
                 color: Tuple[int, int, int],
                 instructions,
                 title_indent_bottom: int,
                 keys_indent_right: int,
                 key_text_font: pygame.font.Font,
                 title_font: pygame.font.Font):
        title_text = title_font.render(title, True, color)

        instruction_surfaces = _get_instruction_surfaces(instructions, key_text_font, color, keys_indent_right)
        instruction_surface = get_surfaces_into_column(instruction_surfaces)

        surface = \
            get_surfaces_into_column([title_text, instruction_surface], Alignment.CENTER, title_indent_bottom)

        super().__init__(surface.get_size())
        super().blit(surface, (0, 0))
