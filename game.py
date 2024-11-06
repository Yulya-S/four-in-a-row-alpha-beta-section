import random
import numpy as np


class four_in_line:
    def __init__(self):
        self.lines = np.array([["X" for _ in range(6)] for _ in range(7)])
        self.step = bool(random.randint(0, 1))

    def play(self):
        end = find_winner(self.lines)
        if end:
            print(f"Поздравляет с победой игрока {end}")
            return False
        pos = int(input(f"Игрок {int(self.step) + 1} введите позицию для хода: "))
        if pos == -1:
            return False
        if pos < 0 or pos > len(self.lines) - 1 or self.lines[pos][-1] != "X":
            print("Сюда нельзя сходить!")
            return self.play()
        else:
            idx = np.where(self.lines[pos] == "X")
            self.lines[pos][idx[0][0]] = "Y" if self.step else "R"
            self.step = not self.step
        return True

    def draw(self):
        print("Y", calculate_price(self.lines, self.step))
        print("R", calculate_price(self.lines, not self.step))
        for i in range(5, -1, -1):
            text = ""
            for l in range(7):
                if len(self.lines[l]) > i:
                    text += f"{self.lines[l][i]}\t"
                else:
                    text += "X\t"
            print(text)


def win_four(line: np.array):
    rem_count = 0
    remember = None
    for i in line:
        if remember is None and i != "X":
            remember = i

        if remember == i:
            rem_count += 1
            if rem_count == 4:
                return remember
        elif i != "X":
            rem_count = 1
            remember = i
    return False


def find_winner(lines: np.array):
    hor = np.column_stack(lines)
    for i in lines:
        result = win_four(i)
        if result:
            return result
    for i in hor:
        result = win_four(i)
        if result:
            return result
    for i in range(-6, 6):
        result = win_four(np.diagonal(lines, i))
        if result:
            return result
    for i in range(-5, 7):
        result = win_four(np.diagonal(np.rot90(lines), i))
        if result:
            return result
    return False


def calculate_four(line: np.array):
    values = [1, 10, 500, 1000]
    result = 0
    count = 0
    rem_count = 0
    remember = None
    for i in line:
        if remember is None and i != "X":
            remember = i

        if i == "X" or remember == i:
            if remember == i:
                rem_count += 1
            count += 1
        else:
            if count >= 4 and rem_count > 0:
                orientacion = 1 if remember == "Y" else -1
                result += values[rem_count - 1] * orientacion
            count = 1
            rem_count = 1
            remember = i
    if count >= 4 and rem_count > 0:
        orientacion = 1 if remember == "Y" else -1
        result += values[rem_count - 1] * orientacion

    return result


def calculate_price(array: np.array, step: bool):
    result = 0
    hor = np.column_stack(array)
    for i in array:
        result += calculate_four(i)
    for i in hor:
        result += calculate_four(i)
    for i in range(-6, 6):
        result += calculate_four(np.diagonal(array, i))
    for i in range(-5, 7):
        result += calculate_four(np.diagonal(np.rot90(array), i))
    if step:
        result *= -1
    return result
