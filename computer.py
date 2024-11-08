from calculations import calculate_price


class Computer:
    def __init__(self, folder: list, player: bool = False):
        self.new_data(folder, player)

    @property
    def hover_idx(self):
        return self.__hover_idx

    @property
    def max_idx(self):
        return self.__max_idx

    def new_data(self, folder: list, player: bool = False):
        self.__folder = folder
        self.__hover_idx = 0
        self.__level = 0
        self.__max_level = 0
        self.__player = player  # true - желтый, false - красный
        self.__max = -1000000
        self.__max_idx = -1

    def step(self):
        if self.__hover_idx < 7:
            if self.__folder[self.__hover_idx].count("X") > 0:
                folder = self.__new_folder(self.__folder, self.__player, self.__hover_idx)
                result = self.__calculate(folder, not self.__player, False)
                if result > self.__max:
                    self.__max = result
                    self.__max_idx = self.__hover_idx
            self.__hover_idx += 1
            if self.__hover_idx >= 7:
                return self.__max_idx
        return None

    def __calculate(self, folder: list, player: bool, regim: bool = True, level: int = 1, idle_value=None):
        # regim = true - ищем max, false - min
        min_max = 1000000 if not regim else -1000000
        for i in range(7):
            if folder[i].count("X") > 0:
                folder = self.__new_folder(folder, player, i)
                if regim and level >= self.__max_level:
                    result = calculate_price(folder)
                    one = 1 if not self.__player else -1
                    result *= one
                else:
                    result = self.__calculate(folder, not player, not regim, level + 1)
                if (regim and min_max < result) or (not regim and min_max > result):
                    min_max = result
        return min_max

    def __new_folder(self, folder: list, player: bool, hover_idx: int):
        f = []
        for i in folder:
            f.append(i.copy())
        if f[hover_idx].count("X") > 0:
            idx = f[hover_idx].index("X")
            f[hover_idx][idx] = "Y" if player else "R"
        return f
