import math
import heapq

# ЗАДАНИЕ 1
def solve_hamming_task():
    print("ЗАДАНИЕ 1")
    text = "Pentium "
    binary = ''.join(format(ord(c), '08b') for c in text)

    def parity_bits_count(data_len):
        k = 0
        while (1 << k) < data_len + k + 1:
            k += 1
        return k

    def hamming_encode(data_bits):
        m = len(data_bits)
        k = parity_bits_count(m)
        n = m + k
        code = [0] * n
        j = 0
        for i in range(1, n + 1):
            if (i & (i - 1)) != 0:  # не степень двойки
                code[i-1] = int(data_bits[j])
                j += 1

        for i in range(k):
            pos = 1 << i
            parity = 0
            for j in range(1, n + 1):
                if j & pos:
                    parity ^= code[j-1]
            code[pos-1] = parity
        return code

    def fix_error(code):
        n = len(code)
        k = math.ceil(math.log2(n+1))
        syndrome = 0
        for i in range(k):
            pos = 1 << i
            parity = 0
            for j in range(1, n+1):
                if j & pos:
                    parity ^= code[j-1]
            if parity:
                syndrome += pos
        if syndrome:
            code[syndrome-1] ^= 1
            return syndrome
        return 0

    #разбиваем на два блока по 32 бита
    block1 = binary[:32]
    block2 = binary[32:64]

    print("Блок1 (исходные 32 бита):", block1)
    encoded1 = hamming_encode(block1)
    encoded1[4] ^= 1  #ошибка в 5-м бите
    err = fix_error(encoded1)
    print("Ошибка исправлена, позиция (1-нумерация):", err)

    print("Блок2 (исходные 32 бита):", block2)
    encoded2 = hamming_encode(block2)
    encoded2[20] ^= 1  #ошибка в 21-м бите
    err = fix_error(encoded2)
    print("Ошибка исправлена, позиция (1-нумерация):", err, "\n")


# ЗАДАНИЕ 2
def solve_distance_task():
    print("ЗАДАНИЕ 2")
    symbols = list("иклмнопр")
    #коды с d >= 2
    codes_d2 = {}
    for i, ch in enumerate(symbols):
        data = format(i, '03b')
        parity = str(bin(i).count('1') % 2)
        codes_d2[ch] = data + parity
    print("Коды с d >= 2:", codes_d2)

    #коды с d >= 3
    def hamming74(i):
        bits = [int(x) for x in format(i, '04b')]
        p1 = bits[0] ^ bits[1] ^ bits[2]
        p2 = bits[1] ^ bits[2] ^ bits[3]
        p3 = bits[0] ^ bits[1] ^ bits[3]
        return ''.join(map(str, bits + [p1, p2, p3]))

    codes_d3 = {ch: hamming74(i) for i, ch in enumerate(symbols)}
    print("Коды с d >= 3:", codes_d3, "\n")


# ЗАДАНИЕ 3
def solve_rle_task():
    print("ЗАДАНИЕ 3")
    s = "aaaaaaaaaaaaaadghttttttttttyikloooooooop"
    orig_size = len(s)  # 40 байт

    def rle_compress(data):
        res = []
        i = 0
        n = len(data)
        while i < n: #ищем повторяющуюся серию (длина >= 2)
            run_len = 1
            while i + run_len < n and data[i + run_len] == data[i]:
                run_len += 1
            if run_len >= 2:
                res.append(run_len)
                res.append(data[i])
                i += run_len
            else: #собираем неповторяющийся блок
                start = i
                while i < n and (i == start or data[i] != data[i-1]):
                    i += 1
                block = data[start:i]
                res.append(0)
                res.append(len(block))
                res.extend(block)
        return res

    compressed = rle_compress(s)
    comp_size = len(compressed)  #каждый элемент - 1 байт

    print("Сжатые данные (список байтов/символов):", compressed)
    print("Исходный размер:", orig_size, "байт")
    print("Сжатый размер:", comp_size, "байт")
    stepen = orig_size / comp_size # степень сжатия
    koef = comp_size / orig_size   # коэффициент сжатия
    print(f"Степень сжатия: {stepen:.2f}")
    print(f"Коэффициент сжатия: {koef:.2f}\n")


# ЗАДАНИЕ 4
def solve_huffman_task():
    print("ЗАДАНИЕ 4")
    freqs = {'A': 2, 'B': 2, 'C': 8, 'D': 11, 'E': 19, 'F': 23, 'G': 35}
    # построение дерева Хаффмана
    heap = [[freq, [sym, ""]] for sym, freq in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    codes = dict(heap[0][1:])
    print("Коды Хаффмана:", codes)

    total = sum(freqs.values())  #100
    avg_len = sum(freqs[s] * len(codes[s]) for s in freqs) / total
    uniform_len = 3  #7 символов -> 3 бита
    print(f"Средняя длина Хаффмана: {avg_len:.2f} бит/символ")
    print(f"Равномерный код: {uniform_len} бит/символ")
    stepen = uniform_len / avg_len  #во сколько раз лучше равномерного
    koef = avg_len / uniform_len  #доля от равномерного
    print(f"Степень сжатия (относительно равномерного): {stepen:.2f}")
    print(f"Коэффициент сжатия: {koef:.2f}\n")


# ЗАДАНИЕ 5
def solve_arithmetic_task():
    print("ЗАДАНИЕ 5")
    probs = {'a': 0.1, 'b': 0.1, 'c': 0.05, 'd': 0.55, 'e': 0.1, 'f': 0.1}
    string = "aecdfb"

    #границы символов
    low, high = 0.0, 1.0
    ranges = {}
    cur = 0.0
    for ch, p in probs.items():
        ranges[ch] = (cur, cur + p)
        cur += p

    #кодирование
    for ch in string:
        w = high - low
        l, h = ranges[ch]
        high = low + w * h
        low = low + w * l

    # число бит = ceil(-log2(длина интервала))
    bits = math.ceil(-math.log2(high - low))
    # середина интервала -> двоичная дробь
    mid = (low + high) / 2
    binary = ""
    for _ in range(bits):
        mid *= 2
        if mid >= 1:
            binary += "1"
            mid -= 1
        else:
            binary += "0"

    print("Интервал: [{:.10f}, {:.10f})".format(low, high))
    print("Двоичный код:", binary, "(длина", bits, "бит)")
    uniform_bits = len(string) * 3  # 6*3=18 бит (3 бита на символ для 6 букв)
    stepen = uniform_bits / bits
    koef = bits / uniform_bits
    print("Равномерный код потребовал бы:", uniform_bits, "бит")
    print(f"Степень сжатия (во сколько раз меньше): {stepen:.2f}")
    print(f"Коэффициент сжатия (доля от равномерного): {koef:.2f}\n")


if __name__ == "__main__":
    solve_hamming_task()
    solve_distance_task()
    solve_rle_task()
    solve_huffman_task()
    solve_arithmetic_task()