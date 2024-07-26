"""
Module for drawing text with pygame.freetype.Font
"""

import pygame
import pygame.freetype

def text_draw(surf: pygame.Surface, \
              dest: tuple[int, int] | pygame.math.Vector2, \
              text: str, \
              fgcolor=None, \
              bgcolor=None, \
              keeplinebreaks=True, \
              font=None) -> None:
    font_default.draw_text(surf, dest, text, fgcolor, bgcolor, keeplinebreaks, font)

def text_render(text: str, fgcolor=None, bgcolor=None, style=None, rotation=0, size=0) -> tuple[pygame.Surface, pygame.Rect]:
    return font_default.render(text, fgcolor, bgcolor, style, rotation, size)

def end():
    pygame.freetype.quit()


class PGWrapFont:
    """
    A wrapper class for pygame.freetype.SysFont
    """
    def __init__(self, name="Consolas", size=16, bold=False, italic=False) -> None:
        self.set_font(name, size, bold, italic)
        self.font.fgcolor = (255, 0, 0)
        self.font.bgcolor = (  0, 0, 0)
        self.linespace_factor = 1.0

    def __str__(self) -> str:
        return f"<PGWrapFont, {self.font.name}>"

    def set_font(self, name, size, bold=False, italic=False) -> None:
        if not pygame.freetype.get_init():
            pygame.freetype.init()
        self.font = pygame.freetype.SysFont(name, size, bold, italic)

    def set_fgcolor(self, color=(255, 0, 0)) -> None:
        self.font.fgcolor = color

    def set_bgcolor(self, color=(0, 0, 0)) -> None:
        self.font.bgcolor = color

    def render(self, text: str, fgcolor=None, bgcolor=None, style=None, rotation=0, size=0) -> tuple[pygame.Surface, pygame.Rect]:
        return self.font.render(text, fgcolor, bgcolor)

    def render_to(self, surf: pygame.Surface, dest: tuple[int, int] | pygame.math.Vector2, text: str, fgcolor=None, bgcolor=None) -> pygame.Rect:
        return self.font.render_to(surf, dest, text, fgcolor, bgcolor)

    def draw_text(self, \
                  surf: pygame.Surface, \
                  dest: tuple[int, int] | pygame.math.Vector2, \
                  text: str, \
                  fgcolor=None, \
                  bgcolor=None, \
                  keeplinebreaks=True, \
                  font: pygame.freetype.Font | None = None) \
                   -> None:

        if font is None:
            font = self.font

        cur_font_origin = font.origin
        font.origin = False

        for i_line, str_line in enumerate(text.splitlines(keeplinebreaks)):
            s_text, r_text = font.render(str_line, fgcolor, bgcolor)

            blit_x = dest[0] + r_text.x
            blit_y = dest[1] + int(font.get_sized_ascender() * self.linespace_factor) - r_text.y \
                     + (i_line * (int(font.get_sized_ascender() * self.linespace_factor) - font.get_sized_descender())) \

            surf.blit(s_text, (blit_x, blit_y))

        font.origin = cur_font_origin


    def get_linespace() -> int:
        return int(font.get_sized_ascender() * self.linespace_factor) - font.get_sized_descender()
        


font_default = PGWrapFont("Roboto Mono Regular", 16)
print(font_default)
