import random
import time
import heapq
from collections import deque



# Генерация графа, содержащего K7 и K3,5
def generate_graph(n, seed=42):
    random.seed(seed)
    k7_vertices = list(range(7))
    k35_left = [7, 8, 9]
    k35_right = [10, 11, 12, 13, 14]
    # Множество рёбер (храним как tuple (min, max))
    edges = set()

    # Добавляем рёбра K7
    for i in range(len(k7_vertices)):
        for j in range(i + 1, len(k7_vertices)):
            u, v = k7_vertices[i], k7_vertices[j]
            edges.add((u, v))
    # Добавляем рёбра K_{3,5}
    for u in k35_left:
        for v in k35_right:
            edges.add((u, v))

    # Целевое количество рёбер
    target_deg = n ** 0.5
    target_edges = int(n * target_deg / 2)
    current_edges = len(edges)
    if target_edges > current_edges:
        while len(edges) < target_edges: # Генерируем случайные пары
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v:
                continue
            if u > v:
                u, v = v, u
            edges.add((u, v))

    #Связность графа
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # компоненты связности
    def bfs(start, visited):
        comp = []
        q = deque([start])
        visited[start] = True
        while q:
            u = q.popleft()
            comp.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return comp

    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            comp = bfs(i, visited)
            components.append(comp)

    # Соединяем компоненты, пока не останется одна
    while len(components) > 1:
        comp1 = components[0]
        comp2 = components[1]
        u = random.choice(comp1)
        v = random.choice(comp2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges:
            edges.add((u, v))
            adj[u].append(v)
            adj[v].append(u)
        components[0].extend(comp2)
        components.pop(1)

    # Перестройка списка смежности окончательно
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    return adj, edges


# Алгоритм Флойда-Уоршелла
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v in edges:
        dist[u][v] = 1
        dist[v][u] = 1

    iterations = 0
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            dik = dist[i][k]
            row_i = dist[i]
            row_k = dist[k]
            for j in range(n):
                iterations += 1
                if row_k[j] != INF and row_i[j] > dik + row_k[j]:
                    row_i[j] = dik + row_k[j]
    return dist, iterations


# Алгоритм Дейкстры
def dijkstra(n, adj, source):
    INF = float('inf')
    dist = [INF] * n
    prev = [-1] * n
    dist[source] = 0
    heap = [(0, source)]
    visited = [False] * n
    extract_count = 0
    relax_count = 0

    while heap:
        d, u = heapq.heappop(heap)
        extract_count += 1
        if visited[u]:
            continue
        visited[u] = True
        if d > dist[u]:
            continue
        for v in adj[u]:
            relax_count += 1
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev, relax_count, extract_count


def reconstruct_path(prev, target):
    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path



# Основная функция для одного размера графа
def process_graph_size(n, run_floyd=True):
    print(f"\n{'=' * 60}")
    print(f"РАЗМЕР ГРАФА: n = {n}")
    print(f"{'=' * 60}")

    # Генерация графа
    start_gen = time.perf_counter()
    adj, edges = generate_graph(n)
    gen_time = time.perf_counter() - start_gen
    m = len(edges)
    avg_deg = 2 * m / n
    sqrt_n = n ** 0.5
    print(f"Генерация: {gen_time:.3f} сек")
    print(f"|V| = {n}, |E| = {m}, средняя степень = {avg_deg:.2f} (целевая ~ {sqrt_n:.2f})")

    # Проверка наличия подграфов K7 и K_{3,5}
    k7_ok = True
    for i in range(7):
        for j in range(i + 1, 7):
            if (i, j) not in edges and (j, i) not in edges:
                k7_ok = False
                break
        if not k7_ok:
            break
    k35_ok = True
    left = [7, 8, 9]
    right = [10, 11, 12, 13, 14]
    for u in left:
        for v in right:
            if (u, v) not in edges and (v, u) not in edges:
                k35_ok = False
                break
        if not k35_ok:
            break
    print(f"Содержит K7: {k7_ok}")
    print(f"Содержит K{'3,5'}: {k35_ok}")


    #1 Алгоритм Флойда-Уоршелла
    if run_floyd and n <= 500:
        print("\n----------------------------- Флойд-Уоршелл -----------------------------")
        start_fw = time.perf_counter()
        dist_fw, fw_iter = floyd_warshall(n, edges)
        fw_time = time.perf_counter() - start_fw
        print(f"Время: {fw_time:.3f} сек")
        print(f"Количество итераций: {fw_iter} (теоретически n^3 = {n ** 3})")
        if n > 1:
            print(f"Расстояние от 0 до {n - 1}: {dist_fw[0][n - 1]}")
    else:
        print("\n----------------------------- Флойд-Уоршелл -----------------------------")
        if not run_floyd:
            print("Пропущен (n > 500, слишком большая сложность)")
        else:
            print(f"Пропущен (n = {n} > 500)")


    #2 Алгоритм Дейкстры

    print("\n----------------------------- Дейкстра от вершины 0 -----------------------------")
    start_dijk = time.perf_counter()
    dist_d, prev_d, relax_cnt, extract_cnt = dijkstra(n, adj, 0)
    dijk_time = time.perf_counter() - start_dijk
    print(f"Время: {dijk_time:.3f} сек")
    print(f"Количество извлечений из кучи: {extract_cnt} (должно быть ~ {n})")
    print(f"Количество релаксаций (итераций алгоритма): {relax_cnt} (2*|E| = {2 * m})")
    if n > 1:
        target = n - 1
        if dist_d[target] < float('inf'):
            path = reconstruct_path(prev_d, target)
            path_len = len(path) - 1
            print(f"Расстояние от 0 до {target}: {dist_d[target]} (рёбер: {path_len})")
            if len(path) <= 20:
                print(f"Путь: {path}")
            else:
                print(f"Путь (первые 10 и последние 10 вершин): {path[:10]} ... {path[-10:]}")
        else:
            print(f"Вершина {target} недостижима из 0 (ошибка связности)")


    # Сравнение с асимптотической сложностью
    print("\n----------------------------- Сравнение с асимптотикой -----------------------------")
    print(f"Флойд-Уоршелл: O(n^3) = {n ** 3} операций (теоретически)")
    if n <= 500 and run_floyd:
        print(f"  Фактически выполнено {fw_iter} операций (n^3 = {n ** 3})")
    else:
        print(f"  Не выполнялся из-за высокой сложности")
    print(f"Дейкстра с двоичной кучей: O((n + m) log n) = {int((n + m) * (n.bit_length()))} операций (теоретически)")
    print(f"  Фактически: {relax_cnt} релаксаций + {extract_cnt} извлечений ≈ {relax_cnt + extract_cnt} операций")



def main():
    sizes = [500, 1500, 4500, 13500, 31000]
    for n in sizes:
        run_floyd = (n == 500)
        process_graph_size(n, run_floyd=run_floyd)


if __name__ == "__main__":
    main()