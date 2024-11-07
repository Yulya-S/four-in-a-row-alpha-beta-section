import numpy as np

def calculate_line_price(lines: list):
    values = [0, 1, 10, 500, 10000]
    result = 0
    for i in lines:
        if len(i) < 4:
            continue
        for l in range(len(i) - 3):
            if i[l:l + 4].count("R") == 0 or i[l:l + 4].count("Y") == 0:
                result += values[i[l:l + 4].count("R")]
                result -= values[i[l:l + 4].count("Y")]
    return result


def field_preparation(field: list):
    fields = [field]
    fields.append(np.column_stack(field).tolist())
    fields.append([])
    for i in range(-6, 6):
        fields[-1].append(np.diagonal(field, i).tolist())
    fields.append([])
    field_rot90 = np.rot90(field)
    for i in range(-5, 7):
        fields[-1].append(np.diagonal(field_rot90, i).tolist())
    return fields


def calculate_price(field: list):
    fields = field_preparation(field)
    result = 0
    for i in fields:
        r = calculate_line_price(i)
        result += r
    return result