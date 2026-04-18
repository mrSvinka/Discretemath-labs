# Задача 1
from collections import Counter

def count_unique_words(target_length, letters_count):
    memo = {}

    def backtrack(current_length, counts_tuple):
        if current_length == 0: # лово нужной длины сформировано
            return 1
        if (current_length, counts_tuple) in memo: # Проверка кэша
            return memo[(current_length, counts_tuple)]

        total_words = 0
        counts_dict = dict(counts_tuple)


        for char, count in counts_dict.items():   # Подстановка букв
            if count > 0:
                counts_dict[char] -= 1
                new_counts_tuple = tuple(sorted(counts_dict.items()))
                total_words += backtrack(current_length - 1, new_counts_tuple)
                counts_dict[char] += 1

        memo[(current_length, counts_tuple)] = total_words
        return total_words

    # Инициализация количества доступных букв
    initial_counts = tuple(sorted(letters_count.items()))
    return backtrack(target_length, initial_counts)


word = "АБРАКАДАБРА"
letters = Counter(word)
result = count_unique_words(6, letters)

print(f"{result}")