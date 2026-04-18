def solve_grid_paths(width, height):

    # Задача 5.1
    dp_simple = [[0] * (height + 1) for _ in range(width + 1)] #количество путей в точку (i, j)
    for i in range(width + 1):
        dp_simple[i][0] = 1  # Движение вправо
    for j in range(height + 1):
        dp_simple[0][j] = 1  # Движение вверх

    for i in range(1, width + 1):
        for j in range(1, height + 1):
            dp_simple[i][j] = dp_simple[i - 1][j] + dp_simple[i][j - 1]

    ans = dp_simple[width][height]

    # Задача 5.2
    dp_h = [[0] * (height + 1) for _ in range(width + 1)] #горезонтальный шаг
    dp_v = [[0] * (height + 1) for _ in range(width + 1)] #Вертикальный

    #Инициализация
    for i in range(1, width + 1):
        dp_h[i][0] = 1
    dp_v[0][1] = 1  #один шаг вверх в начале

    for i in range(1, width + 1):
        for j in range(1, height + 1):
            dp_h[i][j] = dp_h[i - 1][j] + dp_v[i - 1][j]
            dp_v[i][j] = dp_h[i][j - 1]
    ans2 = dp_h[width][height] + dp_v[width][height]

    return ans, ans2


width, height = 19, 16
total_paths, restricted_paths = solve_grid_paths(width, height)

print(f"Кратчайших путей: {total_paths}")
print(f"Путей без 2x вертикальных подряд: {restricted_paths}")