"""
grid.py
dimension is number of axes
range of axe; p.e. -10 to 10
"""

import math



class Grid:
    def __init__(self, size: tuple[int, int] = (10, 7), cell_size: tuple[int, int] = (32, 32)):
        self.width = size[0]
        self.height = size[1]
        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]

    def __str__(self) -> str:
        return f"<Grid, ({self.width}, {self.height}), ({self.cell_width}, {self.cell_height})>"

    def __len__(self) -> int:
        return self.height * self.width

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height

    def get_cell_size(self) -> tuple[int, int]:
        return self.cell_width, self.cell_height

    def get_rect(self, index: int) -> tuple[int, int, int, int]:
        return self.conv_index_to_pos(index) + self.get_cell_size()

    def conv_index_to_coord(self, index: int) -> tuple[int, int]:
        return index % self.width, index // self.width

    def conv_index_to_pos(self, index: int) -> tuple[int, int]:
        return (index % self.width) * self.cell_width, \
               (index // self.width) * self.cell_height

    def conv_coord_to_index(self, coord: tuple[int, int]) -> int:
        return coord[0] + (coord[1] * self.width)

    def conv_coord_to_pos(self, coord: tuple[int, int]) -> tuple[int, int]:
        return coord[0] * self.cell_width, coord[1] * self.cell_height

    def conv_pos_to_index(self, pos: tuple[int | float, int | float]) -> int:
        return int(pos[0] // self.cell_width + ((pos[1] // self.cell_height) * self.width))

    def conv_pos_to_coord(self, pos: tuple[int | float, int | float]) -> tuple[float, float]:
        return pos[0] / self.cell_width, pos[1] / self.cell_height

    def trunc_coord(self, coord: tuple[int | float, int | float]) -> tuple[int, int]:
        return int(coord[0]), int(coord[1])

    def trunc_pos_topleft(self, pos: tuple[int | float, int | float]) -> tuple[int | float, int | float]:
        """ truncate pos to topleft
        """
        return pos[0] % self.cell_width, pos[1] % self.cell_height

    def trunc_step(self, pos: tuple[int, int], step_size: tuple[int, int]) -> tuple[int, int]:
        return (pos[0] // step_size[0]) * step_size[0], \
               (pos[1] // step_size[1]) * step_size[1]

    def is_coord_in_grid(self, coord: tuple[int, int]) -> bool:
        # noinspection PyChainedComparisons
        if coord[0] >= 0 and \
           coord[0] < self.width and \
           coord[1] >= 0 and \
           coord[1] < self.height:
            return True
        else:
            return False

    def dist_vector(self, \
                    this: tuple[int | float, int | float], \
                    other: tuple[int | float, int | float]) -> tuple[int | float, int | float]:
        """vector between this and other
        """
        return other[0] - this[0], other[1] - this[1]

    def dist(self,
             this: tuple[int | float, int | float], \
             other: tuple[int | float, int | float]) -> int | float:
        """ distance beetween this and other
        """
        return math.sqrt(pow(other[0] - this[0], 2) + pow(other[1] - this[1], 2))

    def str_grid(self) -> str:
        string = str()
        pad_id = len(str(len(self)))
        pad_coord = len(str(max(self.width, self.height) - 1))
        index = 0
        for y in range(self.height):
            for x in range(self.width):
                string += f"[{index:{pad_id}}({x:>{pad_coord}}, {y:>{pad_coord}})]"
                index += 1
            string += "\n"
        return string



if __name__ == "__main__":
    grid0 = Grid()
    print(grid0)
    print(grid0.str_grid())
    test_index = 45
    print(f"{test_index=:}")
    print(f"{grid0.conv_index_to_coord(test_index)=:}")
    print(f"{grid0.conv_index_to_pos(test_index)=:}")
    print(f"{grid0.conv_coord_to_index(grid0.conv_index_to_coord(test_index))=:}")
    print(f"{grid0.conv_coord_to_pos(grid0.conv_index_to_coord(test_index))=:}")
    print(f"{grid0.conv_pos_to_index(grid0.conv_index_to_pos(test_index))=:}")
    print(f"{grid0.conv_pos_to_coord(grid0.conv_index_to_pos(test_index))=:}")
    print(f"{grid0.get_rect(test_index)=:}")
