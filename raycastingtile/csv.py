
def csv2d(shape: tuple[int, int], value: int):
    return [[value] * shape[0] for _ in range(shape[1])]

def conv_index(data: tuple[tuple[int]], coord: tuple[int, int]) -> int:
    return (coord[1] * len(data[0])) + coord[0]

def conv_coord(data: tuple[tuple], index: int) -> tuple[int, int]:
    return index % len(data[0]), index // len(data[0])

def str_csv(data: tuple[tuple]) -> str:
    string = str()
    for y in range(len(data)):
        for x in range(len(data[0]) - 1):
            string += f"{data[y][x]}, "
        else:
            string += f"{data[y][-1]}\n"
    return string

def get_csv(data: tuple[tuple[int]], index: int | tuple[int, int]):
    if type(index) is int:
        return data[index // len(data[0])][index % len(data[0])]
    else:
        return data[index[1]][index[0]]

def set_csv(data: tuple[tuple[int]], index: int | tuple[int, int], value: int):
    if type(index) is int:
        data[index // len(data[0])][index % len(data[0])] = value
    else:
        data[index[1]][index[0]] = value

def length(data: tuple[tuple]):
    return len(data) * len(data[0])

def shape(data: tuple[tuple[int]]) -> tuple[int, int]:
    # width, height = len(data[0]), len(data)
    return len(data[0]), len(data)

def save(data: tuple[tuple[int]], filename: str) -> None:
    with open(filename, "w") as file:
        for line in str_csv(data).splitlines(True):
            file.write(line)

def load(filename: str) -> tuple[tuple[int]]:
    with open(filename, "r") as file:
        _list = list()
        for line in file.read().splitlines():
            _list.append([int(x) for x in line.split(", ")])
        return _list





class CSV2D:
    
    def __init__(self, shape: tuple[int, int], value: int):
        self.width = shape[0]
        self.height = shape[1]
        self.data = [value] * (self.height * self.width)

    def __str__(self) -> str:
        return f"<CSV2D, {self.shape()}>"

    def __len__(self) -> int:
        return self.height * self.width

    def __getitem__(self, index: int = 0):
        return self.data[index]

    def __setitem__(self, index: int, value: int):
        self.data[index] = value

    def shape(self) -> tuple[int, int]:
        return self.width, self.height

    def str_csv(self) -> str:
        string = str()
        for y in range(self.height):
            for x in range(self.width - 1):
                string += f"{self.data[(y * self.width) + x]}, "
            else:
                string += f"{self.data[(y * self.width) + (self.width - 1)]}\n"
        return string

    def save(self, filename: str) -> None:
        with open(filename, "w") as file:
            for y in range(self.height):
                for x in range(self.width - 1):
                    file.write(f"{self.data[(y * self.width) + x]}, ")
                else:
                    file.write(f"{self.data[(y * self.width) + (self.width - 1)]}\n")



if __name__ == "__main__":
    # csv2d class
    csv2d0 = CSV2D((5, 3), 0)
    print(csv2d0)
    print(len(csv2d0))
    print(csv2d0.shape())
    print(csv2d0.str_csv())
    csv2d0.save("csv0.txt")
    for i in range(len(csv2d0)):
        csv2d0[i] = i
    print(csv2d0.str_csv())

    # csv2d methods for [[x0, x1, ...], [...], ...]
    csv2d1 = csv2d((5, 3), 0)
    print(csv2d1)
    print(f"{conv_index(csv2d1, (1, 1))=:}")
    print(f"{conv_coord(csv2d1, 6)=:}")
    print(str_csv(csv2d1))
    print(f"{get_csv(csv2d1, 6)=:}")
    for i in range(length(csv2d1)):
        set_csv(csv2d1, i, i)
    print(str_csv(csv2d1))
    save(csv2d1, "csv2d1.txt")
    csv2d1copy = load("csv2d1.txt")
