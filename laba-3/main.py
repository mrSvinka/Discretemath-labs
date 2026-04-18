import math
import heapq
from collections import Counter


#ЗАДАЧА 1
def solve_hamming_task():
    print("ЗАДАНИЕ 1")
    text = "Pentium "
    binary_str = ''.join(format(ord(c), '08b') for c in text)

    def get_hamming_k(m):
        k = 0
        while 2 ** k < m + k + 1: k += 1
        return k

    def encode(data):
        m = len(data);
        k = get_hamming_k(m);
        n = m + k
        res = [0] * n
        j = 0
        for i in range(1, n + 1):
            if (i & (i - 1)) != 0:
                res[i - 1] = int(data[j]);
                j += 1
        for i in range(k):
            pos = 2 ** i
            parity = 0
            for j in range(1, n + 1):
                if j & pos: parity ^= res[j - 1]
            res[pos - 1] = parity
        return res

    def fix_error(bits):
        n = len(bits);
        k = math.ceil(math.log2(n + 1))
        syndrome = 0
        for i in range(k):
            pos = 2 ** i
            parity = 0
            for j in range(1, n + 1):
                if j & pos: parity ^= bits[j - 1]
            if parity: syndrome += pos
        if syndrome:
            bits[syndrome - 1] ^= 1
            return syndrome
        return 0

# Блоки по 32 бита
    b1_raw = binary_str[:32]
    b2_raw = binary_str[32:64]

    b1 = encode(b1_raw)
    b2 = encode(b2_raw)

# Имитация ошибок
    print(f"Блок 1 (32 бита): {b1_raw}")
    b1[4] ^= 1  # 5-й бит (индекс 4)
    err1 = fix_error(b1)
    print(f"Ошибка в Б1 найдена на позиции: {err1}")

    print(f"Блок 2 (32 бита): {b2_raw}")
    b2[20] ^= 1  # 21-й бит (индекс 20)
    err2 = fix_error(b2)
    print(f"Ошибка в Б2 найдена на позиции: {err2}\n")


#ЗАДАЧА 2
def solve_distance_task():
    print("ЗАДАНИЕ 2")
    codes_d2 = {c: format(i, '03b') + str(bin(i).count('1') % 2)
                for i, c in enumerate("иклмнопр")}
    print(f"Коды d>=2: {codes_d2}")



    def get_d3(i):  # Используем проверочную матрицу для генерации
        d = [int(x) for x in format(i, '04b')]
        p1 = d[0] ^ d[1] ^ d[2]
        p2 = d[1] ^ d[2] ^ d[3]
        p3 = d[0] ^ d[1] ^ d[3]
        return "".join(map(str, d + [p1, p2, p3]))

    codes_d3 = {c: get_d3(i) for i, c in enumerate("иклмнопр")}
    print(f"Коды d>=3: {codes_d3}\n")


#ЗАДАЧА 3
def solve_rle_task():
    print("ЗАДАНИЕ 3")
    s = "aaaaaaaaaaaaaadghttttttttttyikloooooooop"
    orig_size = len(s)  # 40 байт
    result = []
    i = 0
    while i < len(s):
        run = 1
        while i + run < len(s) and s[i + run] == s[i]: run += 1
        if run > 1:
            result.extend([run, s[i]])
            i += run
        else:
            non_rep = []
            while i < len(s) and (i + 1 == len(s) or s[i] != s[i + 1]):
                non_rep.append(s[i])
                i += 1
            result.extend([0, len(non_rep)] + non_rep)

    comp_size = len(result)
    print(f"Сжатая строка: {result}")
    print(f"Степень: {orig_size / comp_size:.2f}, Коэффициент: {comp_size / orig_size:.2f}\n")


#ЗАДАЧА 4
def solve_huffman_task():
    print("ЗАДАНИЕ 4")
    freqs = {'A': 2, 'B': 2, 'C': 8, 'D': 11, 'E': 19, 'F': 23, 'G': 35}
    heap = [[f, [s, ""]] for s, f in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for p in lo[1:]: p[1] = '0' + p[1]
        for p in hi[1:]: p[1] = '1' + p[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    codes = dict(heapq.heappop(heap)[1:])
    print(f"Коды: {codes}")

    avg_len = sum(freqs[s] * len(codes[s]) for s in freqs) / 100
    # Сравнение с равномерным (3 бита на символ для 7 знаков)
    print(f"Степень: {3 / avg_len:.2f}, Коэффициент: {avg_len / 3:.2f}\n")


#ЗАДАЧА 5
def solve_arithmetic_task():
    print("ЗАДАНИЕ 5")
    probs = {'a': 0.1, 'b': 0.1, 'c': 0.05, 'd': 0.55, 'e': 0.1, 'f': 0.1}
    string = "aecdfb"

    low, high = 0.0, 1.0
    ranges = {}
    curr = 0.0
    for s, p in probs.items():
        ranges[s] = (curr, curr + p)
        curr += p

    for char in string:
        w = high - low
        l_rel, h_rel = ranges[char]
        high = low + w * h_rel
        low = low + w * l_rel

    print(f"Интервал: [{low:.10f}, {high:.10f})")
    bits = math.ceil(-math.log2(high - low))
    print(f"Биты: {bits}")
    print(f"Степень (отн. 18 бит): {18 / bits:.2f}\n")



if __name__ == "__main__":
    solve_hamming_task()
    solve_distance_task()
    solve_rle_task()
    solve_huffman_task()
    solve_arithmetic_task()