import pygame
from mypygame.pygametemplate import Pygame
from mypygame import drawtext
from mypygame.sprite import Sprite
from mypygame.drawcrosshair import crosshair as draw_crosshair
import grid
import gridcell
import csv
from linecollision import line_collision
from tilecollision import tile_path
import log


class Application(Pygame):
    def __init__(self):
        super().__init__()
        self.grid = grid.Grid((16, 10), (64, 64))
        self.start = pygame.math.Vector2((64, 64))
        self.dest = pygame.math.Vector2((64, 64))
        self.sprites_mouseover: pygame.sprite.Group = pygame.sprite.Group()
        for cell_id in range(len(self.grid)):
            gridcell.GridCell(self.all_sprites, cell_id)
            self.all_sprites.sprites()[-1].rect = pygame.Rect(self.grid.get_rect(cell_id))
            self.all_sprites.sprites()[-1].draw()
        self.blocked = csv.csv2d(self.grid.get_size(), 0)
        self.collision_point = pygame.math.Vector2()
        self.collide_line_enable = True

        log.logging.debug("%s.__init__()" % self)

    def update(self):
        self.set_sprites_mouseover()
        self.set_sprites_blocked()
        self.dest = pygame.math.Vector2(pygame.mouse.get_pos())
        if True:
            self.dest.update(self.grid.trunc_step((int(self.dest.x), int(self.dest.y)), \
                                                  (self.grid.get_cell_size()[0] // 4, \
                                                   self.grid.get_cell_size()[1] // 4)))
        self.start += self.eventhandle_wasd()
        if pygame.mouse.get_rel() != (0, 0):
            self.collide_line_enable = True
        if pygame.mouse.get_pressed()[0]:
            if self.collide_line_enable:
                self.collision_point = line_collision(self.grid, self.blocked, self.start, self.dest)
                self.collision_point *= self.grid.get_cell_size()[0]
                path = tile_path(self.grid.conv_pos_to_coord(self.start), \
                                 self.grid.conv_pos_to_coord(self.dest), \
                                 self.grid.get_size())
                path = [self.grid.conv_coord_to_index(coord) for coord in path]
                for sprite in self.get_sprites():
                    if sprite.cell_id in path:
                        sprite.on_path = True
                    else:
                        sprite.on_path = False
                    sprite.draw()

                self.collide_line_enable = False
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pygame.image.save(self.screen, "screenshot.jpg")

    def render(self):
        self.screen.fill("black")
        # self.render_grid()
        self.all_sprites.draw(self.screen)
        self.draw_pos(self.screen, self.start, pygame.Color("red"))
        self.draw_pos(self.screen, self.dest, pygame.Color("green"))
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.line(self.screen, pygame.Color("ghostwhite"), self.start, self.dest, 1)
            pygame.draw.circle(self.screen, pygame.Color("ghostwhite"), self.collision_point, 4, 0)
        pygame.display.flip()

    def draw_grid(self) -> None:
        cell_fgcolor = pygame.Color("red")
        for cell_id in range(len(self.grid)):
            pygame.draw.rect(self.screen, \
                             cell_fgcolor, \
                             pygame.Rect(self.grid.conv_index_to_pos(cell_id), \
                                         self.grid.get_cell_size()), \
                                         1)
            pos = self.grid.conv_index_to_pos(cell_id)
            pos = pos[0] + 8, pos[1] + 4
            drawtext.text_draw(self.screen, pos, f"{cell_id}", cell_fgcolor)

    def draw_pos(self, \
                 surf: pygame.Surface, \
                 pos: tuple[int, int] | pygame.math.Vector2, \
                 color: pygame.Color) -> None:
        draw_crosshair(surf, color, pos, 32)
        drawtext.text_draw(surf, (pos[0] + 6, pos[1] + 6), f"{pos}", color)

    def set_sprites_mouseover(self) -> None:
        sprites_mouseover_new = pygame.sprite.Group()
        for sprite in self.get_sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                sprites_mouseover_new.add(sprite)
        if len(sprites_mouseover_new):
            sprites_mouseover_new.sprites()[-1].set_mouseover(True)
            self.sprites_mouseover.remove(sprites_mouseover_new.sprites()[-1])
        for sprite in self.sprites_mouseover.sprites():
            sprite.set_mouseover(False)
        self.sprites_mouseover.empty()
        self.sprites_mouseover.add(sprites_mouseover_new)

    def set_sprites_blocked(self) -> None:
        for cell_id, sprite in enumerate(self.get_sprites()):
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[2]:
                    sprite.switch_blocked()
                    csv.set_csv(self.blocked, cell_id, int(sprite.blocked))

    def eventhandle_wasd(self) -> tuple[int, int]:
        step_size = self.grid.get_cell_size()[0] // 4
        velocity = [0, 0]
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            velocity[0] += step_size
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            velocity[0] -= step_size
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            velocity[1] += step_size
        if pygame.key.get_pressed()[pygame.K_UP]:
            velocity[1] -= step_size
        return velocity[0], velocity[1]


app = Application()
app.init()
app.main()
app.end()
