"""
tilecollision.py
2024-06-30
todo:
    when dest is corner point
    a) path somtimes leads through neighbouring tile L shape instead of streight \
    b) no collision with line
    line from tile center to center gives better result
"""

import math
import pygame
import log



def tile_path(start_coord: tuple[int | float, int | float] | pygame.Vector2, \
              dest_coord: tuple[int | float, int | float] | pygame.Vector2, \
              grid_size: tuple[int, int]) \
              -> list[list[int]]:
    """return list of tile coords, located on the line from start to dest
       function use unit vectors only
    """
    log.logging.debug(".tile_path(start_coord: %s, dest_coord: %s" % (start_coord, dest_coord))
    start: pygame.Vector2 = pygame.Vector2(start_coord)
    path: list[list[int]] = [[int(start.x), int(start.y)], ]
    dest: pygame.Vector2 = pygame.Vector2(dest_coord)
    dir: pygame.Vector2 = dest - start
    if any(dir):
        dir.normalize_ip()
    else:
        log.logging.debug("* .tile_path() return: start is dest(?); dir: %s" % repr(dir))
        return path

    if not dir.x:
        step_size = pygame.Vector2(float("inf"), 1)
    elif not dir.y:
        step_size = pygame.Vector2(1, float("inf"))
    else:
        step_size: pygame.Vector2 = pygame.Vector2(math.sqrt(1 + ((dir.y / dir.x) * (dir.y / dir.x))), \
                                                   math.sqrt(1 + ((dir.x / dir.y) * (dir.x / dir.y))))

    step = pygame.Vector2()
    magnitude = pygame.Vector2()
    if dir.x < 0:
        step.x = -1
        magnitude.x = (start.x - path[-1][0]) * step_size.x
    else:
        step.x = 1
        magnitude.x = ((path[-1][0] + 1) - start.x) * step_size.x
    if dir.y < 0:
        step.y = -1
        magnitude.y = (start.y - path[-1][1]) * step_size.y
    else:
        step.y = 1
        magnitude.y = ((path[-1][1] + 1) - start.y) * step_size.y

    log.logging.debug("* init")
    log.logging.debug("start: %s" % (repr(start), ))
    log.logging.debug("dest: %s" % (repr(dest),))
    log.logging.debug("dir: %s" % (repr(dir),))
    log.logging.debug("step_size: %s" % (repr(step_size),))
    log.logging.debug("step: %s" % (repr(step),))
    log.logging.debug("magnitude: %s" % (repr(magnitude),))
    log.logging.debug("path: %s" % (path,))

    i = 0
    max_i = 100
    while not path[-1] == [int(dest.x), int(dest.y)]:
        if magnitude.x < magnitude.y:
            path.append([path[-1][0] + int(step.x), path[-1][1]])
            magnitude.x += step_size.x
        else:
            path.append([path[-1][0], path[-1][1] + int(step.y)])
            magnitude.y += step_size.y

        log.logging.debug("* while iteration %d completed" % i)
        log.logging.debug("magnitude %s" % repr(magnitude))
        log.logging.debug("path[-1] %s  == [int(dest.x) %d, int(dest.y)] %d -> %s" \
                          % (path[-1], int(dest.x), int(dest.y), path[-1] == [int(dest.x), int(dest.y)]))

        if not all((path[-1][0] >= 0, \
                    path[-1][0] < grid_size[0], \
                    path[-1][1] >= 0, \
                    path[-1][1] < grid_size[1])):
            log.logging.debug("* .tile_path() return inexplicable: coord outside grid %s" % (grid_size, ))
            return path[:-1]

        if not i < max_i:
            log.logging.debug("* .tile_path() return inexplicable: max iteration %d/%d reached!" % (i, max_i))
            for i, coord in enumerate(path):
                log.logging.debug("path[%2d] %s" % (i, coord))
            return path
        i += 1

    else:
        log.logging.debug("* .tile_path() return completed")
        for i, coord in enumerate(path):
            log.logging.debug("path[%2d] %s" % (i, coord))
        return path