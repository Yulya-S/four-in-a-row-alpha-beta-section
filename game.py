import random
import pyglet
from calculations import field_preparation, calculate_price
from computer import Computer


# 4-е в ряд
class Game:
    def __init__(self, computers: [bool, bool] = [True, False]):
        self.__folder = [["X" for _ in range(6)] for _ in range(7)]
        self.player: bool = bool(random.randint(0, 1))  # true - Желтые, false - красные
        self.__hover_idx = -1
        self.__computers = computers
        self.__computer = Computer(self.__folder, self.player)
        self.winner = None

    def __search(self, lines: list) -> str:
        for i in lines:
            if len(i) < 4:
                continue
            for l in range(len(i) - 3):
                if i[l:l + 4].count("R") == 4:
                    return "R"
                elif i[l:l + 4].count("Y") == 4:
                    return "Y"
        return "X"

    @property
    def end(self):
        folders = field_preparation(self.__folder)
        for folder in folders:
            result = self.__search(folder)
            if result != "X":
                print(f"Победил игрок {result}")
                self.winner = result
                self.__hover_idx = -1
                return True
        return False

    @property
    def __folder_copy(self):
        f = []
        for i in self.__folder:
            f.append(i.copy())
        return f

    def __calculate_pos(self):
        f = self.__folder_copy
        if f[self.__hover_idx].count("X") > 0:
            idx = f[self.__hover_idx].index("X")
            f[self.__hover_idx][idx] = "Y" if self.player else "R"
        one = 1 if not self.player else -1
        print("Расчет удачности позиции", calculate_price(f) * one)

    def mark_mouse(self, x: int):
        if x < 50 or x > 450 or self.__computers[int(self.player)]:
            return
        circle_pos = 50
        for i in range(len(self.__folder)):
            if x > circle_pos and x < circle_pos + 50:
                self.__hover_idx = i
                return
            circle_pos += 60

    def press(self):
        if self.__hover_idx >= 0 and self.__folder[self.__hover_idx].count("X") > 0 and \
                not self.__computers[int(self.player)]:
            self.__dumping(self.__hover_idx)

    def __dumping(self, dumping_idx: int):
        idx = self.__folder[dumping_idx].index("X")
        self.__folder[dumping_idx][idx] = "Y" if self.player else "R"
        self.player = not self.player
        self.__computer.new_data(self.__folder_copy, self.player)

    def draw(self):
        if not self.winner and self.__computers[int(self.player)]:
            result = self.__computer.step()
            self.__hover_idx = self.__computer.hover_idx
            if result is not None:
                self.__hover_idx = result
                self.__dumping(result)

        color1 = (255, 0, 0)
        color1_mark = (255, 200, 200)

        color2 = (255, 255, 0)
        color2_mark = (255, 255, 200)
        radius = 25
        x = 75
        y = 75
        mark: bool = False
        for i in range(len(self.__folder)):
            for cell in self.__folder[i]:
                pyglet.shapes.Circle(x, y, radius + 1, color=(0, 0, 0)).draw()
                color = (200, 200, 200)
                if cell == "R":
                    color = color1
                elif cell == "Y":
                    color = color2
                elif self.__hover_idx == i and not mark:
                    mark = not mark
                    if not self.player:
                        color = color1_mark
                    else:
                        color = color2_mark
                pyglet.shapes.Circle(x, y, radius, color=color).draw()
                y += radius * 2 + 10
            y = 75
            x += radius * 2 + 10
