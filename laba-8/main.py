"""
Лабораторная работа №8. Вариант 25.
Алгоритм Форда–Фалкерсона (Эдмондс–Карп) для поиска максимального потока
и минимального разреза.
Две сети: исходная и со случайными пропускными способностями [100, 1000].
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque


# ==================== 1. Реализация алгоритма Форда–Фалкерсона ====================
def ford_fulkerson_max_flow(nodes, edges, source='S', sink='T', verbose=True):
    """
    Находит максимальный поток и минимальный разрез.
    Возвращает: max_flow, flow_matrix, steps, cut_edges, visited
    """
    # Индексация вершин
    idx = {name: i for i, name in enumerate(nodes)}
    n = len(nodes)

    # Матрица пропускных способностей
    cap = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        cap[idx[u]][idx[v]] = c

    # Матрица потока (все нули изначально)
    flow = [[0] * n for _ in range(n)]

    max_flow = 0
    steps = []  # (путь в виде индексов, добавленный поток)

    # Основной цикл: пока есть дополняющий путь
    while True:
        # Поиск в ширину кратчайшего пути в остаточной сети
        parent = [-1] * n
        parent[idx[source]] = idx[source]
        q = deque([idx[source]])
        while q:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and cap[u][v] - flow[u][v] > 0:
                    parent[v] = u
                    q.append(v)
                    if v == idx[sink]:
                        break
            else:
                continue
            break

        # Если сток не достигнут – выход
        if parent[idx[sink]] == -1:
            break

        # Восстанавливаем путь и находим "узкое место"
        path = []
        v = idx[sink]
        bottleneck = float('inf')
        while v != idx[source]:
            u = parent[v]
            path.append(v)
            bottleneck = min(bottleneck, cap[u][v] - flow[u][v])
            v = u
        path.append(idx[source])
        path.reverse()

        # Обновляем потоки вдоль пути
        v = idx[sink]
        while v != idx[source]:
            u = parent[v]
            flow[u][v] += bottleneck
            flow[v][u] -= bottleneck  # обратные рёбра
            v = u

        max_flow += bottleneck
        steps.append((path, bottleneck))

        if verbose:
            path_names = [nodes[i] for i in path]
            print(f"   Дополняющий путь: {' → '.join(path_names)}, величина: {bottleneck}")

    # ========== Минимальный разрез ==========
    # Вершины, достижимые из истока в остаточной сети
    visited = [False] * n
    q = deque([idx[source]])
    visited[idx[source]] = True
    while q:
        u = q.popleft()
        for v in range(n):
            if not visited[v] and cap[u][v] - flow[u][v] > 0:
                visited[v] = True
                q.append(v)

    # Формируем рёбра разреза (из S-доли в T-долю в исходной сети)
    cut_edges = []
    for u in range(n):
        for v in range(n):
            if visited[u] and not visited[v] and cap[u][v] > 0:
                cut_edges.append((u, v))

    return max_flow, flow, steps, cut_edges, visited


# ==================== 2. Визуализация ====================
def draw_network(nodes, edges, flow, cut_edges, visited, title=""):
    """Рисует ориентированный граф с подписями поток/ёмкость, выделяет разрез."""
    idx = {name: i for i, name in enumerate(nodes)}
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    for u, v, cap in edges:
        f = flow[idx[u]][idx[v]]
        label = f"{f}/{cap}"
        G.add_edge(u, v, capacity=cap, flow=f, label=label)

    # Позиции вершин для наглядности (можно заменить на spring_layout)
    pos = {
        'S': (-2, 1),
        'p': (-1, 2),
        'a': (-1, 0.5),
        'd': (0, 1.5),
        'k': (1, 2),
        'c': (1, 0.5),
        'b': (2, -0.5),
        'T': (3, 1)
    }

    plt.figure(figsize=(11, 6))
    # Цвета узлов по принадлежности к S- или T-доле
    node_colors = ['#90EE90' if visited[idx[n]] else '#FFB6C1' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900)
    nx.draw_networkx_labels(G, pos, font_size=11)

    # Рёбра: обычные и разрезанные
    cut_set = set()
    for u, v in cut_edges:
        if (nodes[u], nodes[v]) in G.edges():
            cut_set.add((nodes[u], nodes[v]))

    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if (u, v) in cut_set:
            edge_colors.append('red')
            edge_widths.append(2.5)
        else:
            edge_colors.append('gray')
            edge_widths.append(1.2)

    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths,
                           arrowstyle='->', arrowsize=18)

    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# ==================== 3. Функция полного эксперимента ====================
def run_experiment(nodes, edges, title="Сеть"):
    """Запускает расчёт, выводит результаты и рисует граф."""
    print(f"\n===== {title} =====")
    max_flow, flow, steps, cut_edges, visited = ford_fulkerson_max_flow(
        nodes, edges, verbose=True
    )

    print(f"\nМаксимальный поток: {max_flow}")

    idx = {name: i for i, name in enumerate(nodes)}
    # S-доля и T-доля
    s_part = [nodes[i] for i, v in enumerate(visited) if v]
    t_part = [nodes[i] for i, v in enumerate(visited) if not v]
    print(f"S-доля разреза: {s_part}")
    print(f"T-доля разреза: {t_part}")
    print("Рёбра минимального разреза:")
    cut_sum = 0
    for u, v in cut_edges:
        cap = 0
        for e in edges:
            if e[0] == nodes[u] and e[1] == nodes[v]:
                cap = e[2]
                break
        print(f"  {nodes[u]} -> {nodes[v]}  (пропускная способность = {cap})")
        cut_sum += cap
    print(f"Пропускная способность разреза: {cut_sum}  (совпадает с потоком: {cut_sum == max_flow})")

    draw_network(nodes, edges, flow, cut_edges, visited,
                 title=f"{title}\nМаксимальный поток = {max_flow}")


# ==================== 4. Главная программа ====================
if __name__ == "__main__":
    # Узлы сети
    nodes = ['S', 'p', 'd', 'a', 'k', 'c', 'b', 'T']

    # Дуги и их пропускные способности (Вариант 25)
    original_edges = [
        ('S', 'p', 12), ('S', 'd', 61), ('S', 'a', 31),
        ('p', 'k', 21), ('p', 'b', 6),
        ('a', 'd', 12), ('a', 'k', 11), ('a', 'b', 6),
        ('d', 'k', 12), ('d', 'c', 7),
        ('k', 'T', 13),
        ('c', 'T', 71), ('c', 'b', 11),
        ('b', 'T', 51)
    ]

    print("=" * 60)
    print("Лабораторная работа №8. Вариант 25")
    print("Максимальный поток и минимальный разрез (Форд–Фалкерсон)")
    print("=" * 60)

    # Часть 1: исходная сеть
    run_experiment(nodes, original_edges, title="Исходная сеть")

    # Часть 2: случайная сеть
    random.seed(12345)
    random_edges = [(u, v, random.randint(100, 1000)) for u, v, _ in original_edges]
    run_experiment(nodes, random_edges, title="Сеть со случайными пропускными способностями [100, 1000]")