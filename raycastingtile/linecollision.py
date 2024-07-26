"""
Ray Casting in tile map using DDA
javidx9
Youtube
2021-02-28

√ 1² + (opposite/adjoint)² = magnitude of 1 step on adjoint axe (x)
√ 1² + (adjoint/opposite)² = magnitude of 1 step on opposite axe (y)

1) init
   set ray_dir = end - start
   set ray_unit_step_size = √ 1² + (opposite/adjoint)², ...
   set map_check = start
   set ray_length_1d = offset to next tile
   set dist = ?
2) loop
   ray_length_1d.x < ray_length_1d.y
"""

import math
from pygame.math import Vector2
from grid import Grid
import csv
import log



def line_collision(grid: Grid, blocked: list[list[int]], pos_start: tuple[float, float], pos_end: tuple[float, float]):
    """ return list of cell_indices that the line collides with
        function use unit vectors

        Parameters
        ----------
        grid : Grid
        blocked : list[list[int]]
        pos_start : tuple[float, float]
            start→ position
        pos_end : tuple[float, float]
            end→ position

        collision_point : Vector2
            point of first collision between line and blocked tile
        ray_dir : Vector2[float, float]
            normalized ray direction
            end - start
        ray_unit_step_size : Vector2[float, float]
            Scaling factor for unit vector component to magnitude
        map_check : Vector2[int, int]
            current tile coordinates
        ray_length_1d : Vector2[float, float]^
            |ray→^| intersection points with next x- or y-axe
        step : Vector2 (i, j)
            ray direction as orthodiagonal vector; (1|-1, ... )
        dist : float
            temporary save ray_length_1d.x | ray_length_1d.y
    """

    temp_str = f"{grid=:}, blocked ..., {pos_start=:}, {pos_end=:}"
    log.logging.debug(temp_str)

    collision_point = Vector2()
    tile_path = list()

    ray_start: Vector2[float, float] = Vector2(grid.conv_pos_to_coord(pos_start))
    ray_end: Vector2[float, float] = Vector2(grid.conv_pos_to_coord(pos_end))
    ray_dir: Vector2[float, float] = Vector2(ray_end) - ray_start
    if any(ray_dir):
        ray_dir.normalize_ip()
    else:
        collision_point = pos_start
        return collision_point

    if not ray_dir.x:
        ray_unit_step_size = Vector2(float("inf"), 1)
    elif not ray_dir.y:
        ray_unit_step_size = Vector2(1, float("inf"))
    else:
        ray_unit_step_size: Vector2[float, float] = Vector2(math.sqrt(1 + ((ray_dir.y / ray_dir.x) * (ray_dir.y / ray_dir.x))), \
                                                            math.sqrt(1 + ((ray_dir.x / ray_dir.y) * (ray_dir.x / ray_dir.y))))
    map_check: Vector2[int, int] = Vector2(grid.trunc_coord(ray_start))
    tile_path.append(map_check.copy())
    ray_length_1d: Vector2[float, float] = Vector2()

    step: Vector2[int, int] = Vector2()

    if ray_dir.x < 0:
        step.x = -1
        ray_length_1d.x = (ray_start.x - map_check.x) * ray_unit_step_size.x
    else:
        step.x = 1
        ray_length_1d.x = ((map_check.x + 1) - ray_start.x) * ray_unit_step_size.x
    if ray_dir.y < 0:
        step.y = -1
        ray_length_1d.y = (ray_start.y - map_check.y) * ray_unit_step_size.y
    else:
        step.y = 1
        ray_length_1d.y = ((map_check.y + 1) - ray_start.y) * ray_unit_step_size.y

    dist: float = 0.0

    log.logging.debug("* init line collision")
    log.logging.debug("collision_point: %s" %(repr(collision_point), ))
    log.logging.debug("ray_end: %s" % (repr(ray_end), ))
    log.logging.debug("ray_start: %s" % (repr(ray_start), ))
    log.logging.debug("ray_dir: %s" % (repr(ray_dir),))
    log.logging.debug("ray_unit_step_size: %s" % (repr(ray_unit_step_size), ))
    log.logging.debug("map_check: %s" % (repr(map_check), ))
    log.logging.debug("step: %s" % (repr(step), ))
    log.logging.debug("ray_length_1d: %s" % (repr(ray_length_1d),))

    while True:
        log.logging.debug("map_check: %s" % (repr(map_check),))
        log.logging.debug("ray_length_1d: %s" % (repr(ray_length_1d),))
        if map_check == grid.trunc_coord(ray_end):
            log.logging.debug("ray reaches end coord: %s" % (repr(ray_end), ))
            break
        if False in (map_check.x >= 0, map_check.x < len(blocked[0]), map_check.y >= 0, map_check.y < len(blocked)):
            log.logging.debug("ray reaches grid border!")
            break
        if csv.get_csv(blocked, (int(map_check[0]), int(map_check[1]))):
            log.logging.debug("ray collide with blocked tile")
            collision_point = ray_start + (ray_dir * dist)
            log.logging.debug("collision point: ray_start %s + (ray_dir %s * dist %.3f) = %s" % (repr(ray_start), repr(ray_dir), dist, repr(collision_point)))
            break

        if ray_length_1d.x < ray_length_1d.y:
            map_check.x += step.x
            dist = ray_length_1d.x
            ray_length_1d.x += ray_unit_step_size.x
        else:
            map_check.y += step.y
            dist = ray_length_1d.y
            ray_length_1d.y += ray_unit_step_size.y
        tile_path.append(map_check.copy())
        log.logging.debug("while iteration end")

    for i, node in enumerate(tile_path):
        log.logging.debug("%d %s" % (i, repr(node)))

    return collision_point