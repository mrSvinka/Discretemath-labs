import collections
import heapq
import math
import os

# 1. Чтение текста
def read_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


# 2. Таблица частот символов и биграмм
def print_frequencies(text):
    total = len(text)
    freq = collections.Counter(text)
    print("\nЧастоты символов")
    print(f"{'Символ':<10} {'Кол-во':<10} {'Частота, %':<10}")
    for ch, cnt in sorted(freq.items(), key=lambda x: -x[1]):
        pct = 100 * cnt / total
        disp = repr(ch)[1:-1] if ch in '\n\r\t' else ch
        print(f"{disp:<10} {cnt:<10} {pct:<10.2f}")

    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_freq = collections.Counter(bigrams)
    print("\nЧастоты биграмм (первые 20)")
    print(f"{'Биграмма':<10} {'Кол-во':<10} {'Частота, %':<10}")
    for bg, cnt in sorted(bigram_freq.items(), key=lambda x: -x[1])[:20]:
        pct = 100 * cnt / (total - 1)
        print(f"{repr(bg)[1:-1]:<10} {cnt:<10} {pct:<10.2f}")


# 3. Энтропия и количество информации
def entropy_and_info(text):
    freq = collections.Counter(text)
    n = len(text)
    ent = 0.0
    for cnt in freq.values():
        p = cnt / n
        if p > 0:
            ent -= p * math.log2(p)
    return ent, ent * n


# 4. Кодирование Хаффмана
def huffman_encode(text):
    freq = collections.Counter(text)
    heap = [[cnt, [ch, ""]] for ch, cnt in freq.items()]
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
    encoded = ''.join(codes[ch] for ch in text)
    return encoded, len(encoded)


# 5. Кодирование LZW
def lzw_encode(text, max_dict_size=4096, code_bits=12):
    # Переводим текст в байты (UTF-8)
    data = text.encode('utf-8')
    # Начальный словарь: байт -> код (0..255)
    dictionary = {bytes([i]): i for i in range(256)}
    next_code = 256
    codes = []
    if not data:
        return "", 0

    current = bytes([data[0]])
    for b in data[1:]:
        nxt = current + bytes([b])
        if nxt in dictionary:
            current = nxt
        else:
            codes.append(dictionary[current])
            if next_code < max_dict_size:
                dictionary[nxt] = next_code
                next_code += 1
            current = bytes([b])
    codes.append(dictionary[current])

    total_bits = len(codes) * code_bits
    bit_string = ''.join(format(c, '0{}b'.format(code_bits)) for c in codes)
    return bit_string, total_bits


# 6. Сохранение битовой строки в файл (первые N символов)
def save_bits(filename, bits, max_len=5000):
    content = bits[:max_len] + (f"\n... и ещё {len(bits)-max_len} бит" if len(bits) > max_len else "")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Сохранено в {filename} (показано {min(len(bits), max_len)} бит)")


# 7. Главная функция
def main():
    if not os.path.exists("text.txt"):
        print("Файл text.txt не найден")
        return

    text = read_text("text.txt")
    print(f"Загружено символов: {len(text)}")

    # Таблицы частот
    print_frequencies(text)

    # Энтропия и информация
    entropy, info = entropy_and_info(text)
    print(f"\nЭнтропия: {entropy:.4f} бит/символ")
    print(f"Количество информации: {info:.2f} бит")

    # Равномерное кодирование (8 бит/символ)
    uniform_bits = len(text) * 8
    print(f"Исходный размер (равномерное 8 бит): {uniform_bits} бит")

    # Хаффман
    huff_bits_str, huff_bits = huffman_encode(text)
    save_bits("encoded_huffman.txt", huff_bits_str)
    ratio_h = huff_bits / uniform_bits
    print(f"\nХаффман: размер = {huff_bits} бит, коэффициент сжатия = {ratio_h:.4f}")

    # LZW
    lzw_bits_str, lzw_bits = lzw_encode(text)
    save_bits("encoded_lzw.txt", lzw_bits_str)
    ratio_l = lzw_bits / uniform_bits
    print(f"LZW: размер = {lzw_bits} бит, коэффициент сжатия = {ratio_l:.4f}")

    # Итоговое сравнение
    print("\nСравнение")
    print(f"Хаффман экономит {100*(1-ratio_h):.2f}%")
    print(f"LZW экономит {100*(1-ratio_l):.2f}%")
    if huff_bits < lzw_bits:
        print("Вывод: Хаффман эффективнее LZW для данного текста.")
    elif huff_bits > lzw_bits:
        print("Вывод: LZW эффективнее Хаффмана для данного текста.")
    else:
        print("Вывод: эффективность одинакова.")

if __name__ == "__main__":
    main()