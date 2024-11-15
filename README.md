## Алгоритм работы
1. Последовательно делаем предположительные ходы игроков.
2. Доходим до хода максимальной глудины (в программе максимальная глубина равна 6 шагам)
3. Расчитываем цену позиции.
5. Оцениваем все полученные результаты для 6 уровня и лучший (с максимальным значением) отправляем на уровень выше.
6. Оцениваем все результаты на уровне 5 и отправляем минимальное значение на 4-й уровень.
7. И так продолжаем оценку до 1-го уровня, применяя к каждому четному уровню функцию альфа-бето сечение.

### Альфа-бето сечение:
1. если уровень четный и не максимальный получаем и сохраняем результат прохождения первой ветки
2. к расчету второй ветви применяем проверку: если полученное значение > сохраненого значения, то ветка не рассматривается.
3. В случае если результат < сохраненого значения, то сохраняем и используем далее уже это значение.

### Расчет цены позиции:
1. Берем все возможные четверки на поле (по вертикали, горизонтали, диагонали)
2. Считаем количество красных и количество желтых фишек в четверке
3. Если в четверке есть фишки только одного цвета, то их количество умножаем на константные значения (1 фишка - 1 балл, 2 фишки - 10 баллов, 3 фишки - 500 баллов, 4 фишки - 1000)
4. Если фишки в комбинации были желтыми то умножаем результат предыдущего шага на -1
