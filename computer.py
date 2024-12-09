from calculations import calculate_price, field_preparation
import json
import time


# Компьютер
class Computer:
    def __init__(self, player: bool = False):
        self.__greate_path = []
        self.__folder_base = {}
        self.__folder = [["X" for _ in range(6)] for _ in range(7)]
        self.new_data(-1, player)
        # self.__load_folder_base()

    # Подгрузка обработанных позиций (при включении уменьшает время обработки ходов, которые она раньше уже отыгрывала)
    def __load_folder_base(self):
        with open("base.json", "r") as file:
            self.__folder_base = json.loads(file.read())
        print(self.__folder_base)

    @property
    def folder_base(self):
        return self.__folder_base

    # Получение проверяемой позиции (нужна для отрисовки)
    @property
    def hover_idx(self):
        return self.__hover_idx

    # Очистка данных для нового использования
    def new_data(self, move: int, player: bool = False):
        self.timer = time.time()
        if move > -1:
            self.__folder = self.__new_folder(self.__folder, not player, move)
        self.__find_step = False
        self.__hover_idx = 0
        self.__idle_value = None
        self.__level = 0
        self.__max_level = 5  # Учитываются только свои ходы
        self.__player = player  # true - желтый, false - красный
        if len(self.__greate_path) > 2:
            if self.__greate_path[0] == move:
                self.__hover_idx = self.__greate_path.pop(0)
                self.__find_step = True
            else:
                self.__greate_path = []
        self.__values = []
        self.__pathes = []

    # Проверка компьютером одной возможной позиции
    def step(self):
        if self.__find_step:
            return self.__greate_path[0]

        if self.__hover_idx < 7:
            if self.__folder[self.__hover_idx].count("X") > 0:
                folder = self.__new_folder(self.__folder, self.__player, self.__hover_idx)

                if str(folder) in self.__folder_base.keys():
                    print(self.__folder_base[str(folder)])
                    result = self.__folder_base[str(folder)]
                else:
                    end = self.__end(folder)
                    if end != None:
                        result = self.__calculate(folder, not self.__player, False, self.__max_level + 1,
                                                  self.__idle_value)
                    else:
                        result = self.__calculate(folder, not self.__player, False, 1, self.__idle_value)
                self.__values.append(result[0])
                self.__pathes.append([self.__hover_idx] + result[1])
                if self.__idle_value == None or self.__idle_value < max(self.__values):
                    self.__idle_value = max(self.__values)
            self.__hover_idx += 1
            if self.__hover_idx >= 7:
                idx = self.__values.index(max(self.__values))
                self.__greate_path = self.__pathes[idx]
                print(self.__greate_path)
                return self.__greate_path[0]
        return None

    # Рачет компьютером в глубину
    def __calculate(self, folder: list, player: bool, regim: bool = True, level: int = 1, idle_value=None):
        values = []
        pathes = []

        if str(folder) in self.__folder_base.keys():
            return self.__folder_base[str(folder)]

        # regim = true - ищем max, false - min
        for i in range(7):
            if time.time() - self.timer >= 25.:
                raise Exception("Привышен лимит времени расчета хода")
            if folder[i].count("X") > 0:
                copy_folder = self.__new_folder(folder, player, i)
                end = self.__end(copy_folder)
                if (regim and level >= self.__max_level) or end != None:
                    result = calculate_price(copy_folder)
                    one = 1 if not self.__player else -1
                    result *= one
                    values.append(result)
                    pathes.append([i])
                    if idle_value != None and result > idle_value:
                        break
                else:
                    result = self.__calculate(copy_folder, not player, not regim, level + 1, idle_value)
                    if result == None:
                        result = calculate_price(copy_folder)
                        one = 1 if not self.__player else -1
                        result *= one
                        values.append(result)
                        pathes.append([i])
                    else:
                        values.append(result[0])
                        pathes.append([i] + result[1])
                    if regim and (idle_value == None or idle_value > max(values)):
                        idle_value = max(values)
                    elif not regim and idle_value != None and idle_value > min(values):
                        break
        if time.time() - self.timer >= 25.:
            raise Exception("Привышен лимит времени расчета хода")
        if len(values) == 0:
            return None
        idx = values.index(max(values) if regim else min(values))
        self.__folder_base[str(folder)] = [values[idx], pathes[idx]]
        return [values[idx], pathes[idx]]

    # Проверка наличия победителя
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

    # Проверка на окончание игры
    def __end(self, copy_folder):
        folders = field_preparation(copy_folder)
        for folder in folders:
            result = self.__search(folder)
            if result != "X":
                return result == "R"
        return None

    # Создание копии поля, с одним дополнительным шагом
    def __new_folder(self, folder: list, player: bool, hover_idx: int):
        f = []
        for i in folder:
            f.append(i.copy())
        if f[hover_idx].count("X") > 0:
            idx = f[hover_idx].index("X")
            f[hover_idx][idx] = "Y" if player else "R"
        return f
