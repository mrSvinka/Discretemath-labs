from collections import Counter
from math import log2, ceil
import heapq

#Загрузка текста 
with open('text.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()
print(f"Исходный текст: {len(raw_text)} символов")

#Не более 64 частых символов оставим
cnt = Counter(raw_text)
top_chars = [ch for ch, _ in cnt.most_common(64)]
keep = set(top_chars)
text = ''.join(c if c in keep else top_chars[0] for c in raw_text)
print(f"После фильтрации: {len(text)} символов, уникальных: {len(set(text))}")

#Статистический анализ
char_freq = Counter(text)
total = len(text)
print("\nТоп-10 символов:")
for ch, fr in char_freq.most_common(10):
    print(f"  '{ch}': {fr:5d} ({fr/total:.4f})")

bigram_freq = Counter(text[i:i+2] for i in range(total-1))
print("\nТоп-10 биграмм:")
for bg, fr in bigram_freq.most_common(10):
    print(f"  \"{bg}\": {fr:5d} ({fr/(total-1):.4f})")

#Код Хаффмана
class Node:
    __slots__ = ('char', 'freq', 'left', 'right')
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right
    def __lt__(self, other):
        return self.freq < other.freq

heap = [Node(ch, f) for ch, f in char_freq.items()]
heapq.heapify(heap)
while len(heap) > 1:
    a, b = heapq.heappop(heap), heapq.heappop(heap)
    heapq.heappush(heap, Node(freq=a.freq + b.freq, left=a, right=b))

def make_codes(node, prefix='', codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        make_codes(node.left, prefix + '0', codebook)
        make_codes(node.right, prefix + '1', codebook)
    return codebook

codes = make_codes(heap[0])
huff_bits = len(''.join(codes[ch] for ch in text))
uniform_bits = total * 6
print(f"\nХаффман: {huff_bits} бит")
print(f"Равномерный 6-бит: {uniform_bits} бит")
print(f"Сжатие: {100*(1 - huff_bits/uniform_bits):.2f}%")

# Энтропия Шеннона
H = -sum((f/total) * log2(f/total) for f in char_freq.values())
info_bits = total * H
print(f"Энтропия: {H:.4f} бит/символ, количество информации: {info_bits:.0f} бит")
print(f"Избыточность Хаффмана: {huff_bits/total - H:.4f} бит/символ")

#LZW
distinct = sorted(set(text))
dict_size = len(distinct)
dictionary = {ch: i for i, ch in enumerate(distinct)}
code_width = max(1, ceil(log2(dict_size)))
next_code = dict_size
lzw_bits = 0
w = ''
for c in text:
    wc = w + c
    if wc in dictionary:
        w = wc
    else:
        lzw_bits += code_width
        if next_code < 8192:  # верхняя граница словаря
            dictionary[wc] = next_code
            next_code += 1
            if next_code > (1 << code_width):
                code_width += 1
        w = c
if w:
    lzw_bits += code_width

print(f"\nLZW (8192 гнезда): {lzw_bits} бит")
print(f"Сжатие LZW отн. равномерного: {100*(1 - lzw_bits/uniform_bits):.2f}%")
print(f"Сжатие LZW отн. Хаффмана: {100*(1 - lzw_bits/huff_bits):.2f}%")

print("\n" + "-"*81)
print(f"Символов в тексте: {total}")
print(f"Разных символов:    {len(set(text))}")
print(f"Равномерный (6 бит): {uniform_bits} бит")
print(f"Хаффман:            {huff_bits} бит")
print(f"LZW:                {lzw_bits} бит")
print(f"Информация Шеннона:  {info_bits:.0f} бит")
print("-"*81)