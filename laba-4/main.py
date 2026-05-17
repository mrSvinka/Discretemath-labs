import collections
import heapq
import math
import os
import re

#0 Чтение текста
def read_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


#1 Таблица частот символов и пар
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
    print("\nЧастоты пар (первые 20)")
    print(f"{'Пары':<10} {'Кол-во':<10} {'Частота, %':<10}")
    for bg, cnt in sorted(bigram_freq.items(), key=lambda x: -x[1])[:20]:
        pct = 100 * cnt / (total - 1)
        print(f"{repr(bg)[1:-1]:<10} {cnt:<10} {pct:<10.2f}")


#Энтропия и количество информации
def entropy_and_info(text):
    freq = collections.Counter(text)
    n = len(text)
    ent = 0.0
    for cnt in freq.values():
        p = cnt / n
        if p > 0:
            ent -= p * math.log2(p)
    return ent, ent * n


#2 Кодирование Хаффмана
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


#3 Кодирование LZW
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


#Сохранение битовой строки в файл
def save_bits(filename, bits):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(bits)
    print(f"Сохранено в {filename}")


def filter_text(text, to_lower=False):
    allowed = r"[A-Za-z0-9 .,!?;:()'\"-]"
    filtered = ''.join(re.findall(allowed, text))
    if to_lower:
        filtered = filtered.lower()
    return filtered





def main():
    if not os.path.exists("text.txt"):
        print("Файл text.txt не найден")
        return

    text = read_text("text.txt")
    print(f"Загружено символов: {len(text)}")

    unique_chars = set(text)
    unique_count = len(unique_chars)
    print(f"Количество уникальных символов: {unique_count}")

    if unique_count > 64:
        print(f"\nКоличество уникальных символов ({unique_count}) > 64.")
        print("Выполняется фильтрация.")
        text = filter_text(text, to_lower=True)
        unique_count = len(set(text))
        print(f"После фильтрации: ({unique_count}) уникальных символов ")
        if unique_count > 64:
            print("Ошибка")
            return

    print_frequencies(text)

    entropy, info = entropy_and_info(text)
    print(f"\nЭнтропия: {entropy:.4f} бит/символ")
    print(f"Количество информации: {info:.2f} бит")

    uniform_bits = len(text) * 6
    print(f"Исходный размер (равномерное 6 бит): {uniform_bits} бит")

    huff_bits_str, huff_bits = huffman_encode(text)
    save_bits("encoded_huffman.txt", huff_bits_str)
    ratio_huff = uniform_bits / huff_bits
    print(f"Хаффман: размер = {huff_bits} бит, коэффициент сжатия = {ratio_huff:.4f}")

    lzw_bits_str, lzw_bits = lzw_encode(text)
    save_bits("encoded_lzw.txt", lzw_bits_str)
    ratio_lzw = uniform_bits / lzw_bits
    print(f"LZW: размер = {lzw_bits} бит, коэффициент сжатия = {ratio_lzw:.4f}")

    print("\nСравнение")
    ratio_h = huff_bits / uniform_bits
    print(f"Хаффман экономит {100*(1-ratio_h):.2f}%")
    ratio_l = lzw_bits / uniform_bits
    print(f"LZW экономит {100*(1-ratio_l):.2f}%")
    if huff_bits < lzw_bits:
        print("Вывод: Хаффман эффективнее.")
    elif huff_bits > lzw_bits:
        print("Вывод: LZW эффективнее.")
    else:
        print("Вывод: эффективность одинакова.")

if __name__ == "__main__":
    main()