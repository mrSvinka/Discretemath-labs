import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

# Исходные рёбра
edges = [(3,8), (4,7), (4,8), (4,11), (4,14), (5,7), (5,8), (6,7), (6,8),
         (6,14), (6,15), (7,9), (7,10), (7,13), (7,16), (7,17), (8,12),
         (9,15), (11,13), (11,17), (12,14), (12,15), (14,17), (15,16)]

# 1. Проверка двудольности и получение долей
def bipartite_sets(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    color = {}
    for start in adj:
        if start in color:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return None   # не двудольный
    left = [v for v, c in color.items() if c == 0]
    right = [v for v, c in color.items() if c == 1]
    return left, right

left, right = bipartite_sets(edges)
print("Двудольный:", left is not None)
if left:
    print("Доля A:", sorted(left))
    print("Доля B:", sorted(right))
else:
    print("Граф не двудольный. Удаление рёбер не требуется (по факту граф двудольный).")

# 2. Алгоритм Форда‑Фалкерсона (через потоковую сеть)
def max_matching_ff(edges, left, right):
    L, R = len(left), len(right)
    id = {v: i for i, v in enumerate(left)}
    id.update({v: L + i for i, v in enumerate(right)})
    source, sink = L + R, L + R + 1
    cap = [[0] * (sink + 1) for _ in range(sink + 1)]
    for u, v in edges:
        if u in left and v in right:
            cap[id[u]][id[v]] = 1
        elif v in left and u in right:
            cap[id[v]][id[u]] = 1
    for u in left:
        cap[source][id[u]] = 1
    for v in right:
        cap[id[v]][sink] = 1

    parent = [-1] * (sink + 1)
    def bfs():
        for i in range(sink + 1):
            parent[i] = -1
        parent[source] = source
        q = deque([source])
        while q:
            u = q.popleft()
            for v in range(sink + 1):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    if v == sink:
                        return True
                    q.append(v)
        return False

    flow = 0
    while bfs():
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        flow += 1

    matching = []
    for u in left:
        for v in right:
            if cap[id[v]][id[u]] == 1 and cap[id[u]][id[v]] == 0:
                matching.append((u, v))
    return matching

# 3. Алгоритм Куна (увеличивающие цепи)
def max_matching_kuhn(edges, left, right):
    adj = {u: [] for u in left}
    for u, v in edges:
        if u in left and v in right:
            adj[u].append(v)
        elif v in left and u in right:
            adj[v].append(u)
    match_r = {v: None for v in right}
    def dfs(u, seen):
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                if match_r[v] is None or dfs(match_r[v], seen):
                    match_r[v] = u
                    return True
        return False
    for u in left:
        seen = {v: False for v in right}
        dfs(u, seen)
    return [(u, v) for v, u in match_r.items() if u is not None]

if left:
    match_ff = max_matching_ff(edges, left, right)
    match_kuhn = max_matching_kuhn(edges, left, right)
    print("\nПаросочетание (Форд‑Фалкерсон):", sorted(match_ff))
    print("Паросочетание (Кун):", sorted(match_kuhn))
    print("Размер:", len(match_ff))

# 4. Визуализация (с сохранением рисунка)
if left:
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, nodelist=left, node_color='lightblue', label='Доля A')
    nx.draw_networkx_nodes(G, pos, nodelist=right, node_color='lightgreen', label='Доля B')
    nx.draw_networkx_edges(G, pos, edgelist=edges, alpha=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=match_ff, edge_color='red', width=2)
    nx.draw_networkx_labels(G, pos)
    plt.legend()
    plt.title("Максимальное паросочетание в двудольном графе")
    plt.axis('off')
    plt.savefig("matching_visualization.png")
    plt.show()