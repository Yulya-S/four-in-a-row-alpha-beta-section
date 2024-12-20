from calculations import calculate_price


# Компьютер
class Computer:
    def __init__(self, folder: list, player: bool = False):
        self.new_data(folder, player)

    # Получение проверяемой позиции (нужна для отрисовки)
    @property
    def hover_idx(self):
        return self.__hover_idx

    # Очистка данных для нового использования
    def new_data(self, folder: list, player: bool = False):
        self.__folder = folder
        self.__hover_idx = 0
        self.__level = 0
        self.__max_level = 3
        self.__player = player  # true - желтый, false - красный
        self.__max = -1000000
        self.__max_idx = -1

    # Проверка компьютером одной возможной позиции
    def step(self):
        if self.__hover_idx < 7:
            if self.__folder[self.__hover_idx].count("X") > 0:
                folder = self.__new_folder(self.__folder, self.__player, self.__hover_idx)
                result = self.__calculate(folder, not self.__player, False, 1, self.__max)
                if result > self.__max:
                    self.__max = result
                    self.__max_idx = self.__hover_idx
            self.__hover_idx += 1
            if self.__hover_idx >= 7:
                return self.__max_idx
        return None

    # Рачет компьютером в глубину
    def __calculate(self, folder: list, player: bool, regim: bool = True, level: int = 1, idle_value=None):
        # regim = true - ищем max, false - min
        min_max = 1000000 if not regim else -1000000
        for i in range(7):
            if folder[i].count("X") > 0:
                copy_folder = self.__new_folder(folder, player, i)
                if regim and level >= self.__max_level:
                    result = calculate_price(copy_folder)
                    one = 1 if not self.__player else -1
                    result *= one
                else:
                    result = self.__calculate(copy_folder, not player, not regim, level + 1, idle_value)
                if (regim and min_max < result) or (not regim and min_max > result):
                    min_max = result
                    # функция альфа-бета сечения
                    if regim:
                        if min_max > idle_value and level < self.__max_level:
                            # print(f"новый idle {idle_value} -> {min_max}")
                            idle_value = min_max
                        elif idle_value != -1000000 and min_max > idle_value:
                            # print(f"отсекаем ветку {idle_value} < {min_max}", level, i)
                            return min_max
        return min_max

    # Создание копии поля, с одним дополнительным шагом
    def __new_folder(self, folder: list, player: bool, hover_idx: int):
        f = []
        for i in folder:
            f.append(i.copy())
        if f[hover_idx].count("X") > 0:
            idx = f[hover_idx].index("X")
            f[hover_idx][idx] = "Y" if player else "R"
        return f
