import pygame
import mypygame



class GridCell(mypygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, cell_id: int):
        super().__init__(group)
        self.cell_id: int = cell_id
        self.on_path: bool = False
        self.blocked: bool = False
        self.mouseover: bool = False
        self.draw()

    def draw(self):
        if self.blocked:
            fgcolor = pygame.Color("lightsalmon")
            bgcolor = pygame.Color("lightsalmon3")
        elif self.on_path:
            fgcolor = pygame.Color("palegreen")
            bgcolor = pygame.Color("palegreen4")
        else:
            fgcolor = pygame.Color("darkslategray4") # deepskyblue1
            bgcolor = pygame.Color("darkslategrey") # dodgerblue4
        if self.mouseover:
            fgcolor = pygame.Color("gold1")
        self.image.fill(bgcolor)
        pygame.draw.rect(self.image, fgcolor, pygame.Rect((0, 0), self.image.get_size()), 1)
        self_coord = self.rect.x // self.rect.w, self.rect.y // self.rect.h
        mypygame.drawtext.text_draw(self.image, (4, 4), f"{self.cell_id}\n" + f"{self_coord[0]}/{self_coord[1]}", fgcolor, bgcolor)

    def switch_blocked(self):
        self.blocked = not self.blocked
        self.draw()

    def set_mouseover(self, state: bool):
        if self.mouseover != state:
            self.mouseover = state
            self.draw()