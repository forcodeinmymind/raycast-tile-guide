import pygame



def crosshair(source: pygame.Surface, \
              color: pygame.Color | tuple[int, int, int, int] = (255, 0, 0, 255), \
              dest: tuple[int, int] = (0, 0), \
              size: int = 32) \
              -> None:

    pygame.draw.line(source, color, (dest[0] - (size // 2), dest[1]), (dest[0] + (size // 2), dest[1]))
    pygame.draw.line(source, color, (dest[0], dest[1] - (size // 2)), (dest[0], dest[1] + (size // 2)))
