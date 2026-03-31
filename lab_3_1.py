import math
from collections import Counter

name = "СЛІПЕЦЬІВАНДМИТРОВИЧ"
n = len(name)

#  Розрахунок частот та ймовірностей
freq = Counter(name)
# Сортуємо для зручності аналізу
sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
probs = {char: count/n for char, count in sorted_items}
formatted_probs = {char: f"{p:.3f}" for char, p in probs.items()}

# Безумовна ентропія за Шенноном (H)
h = -sum(p * math.log2(p) for p in probs.values())

# 1.4 Кодовий словник Хаффмана
huffman_codes = {
    'І': '00', 'В': '010', 'Н': '011', 'Т': '100', 'И': '101', 
    'С': '11000', 'Л': '11001', 'П': '11010', 'Е': '11011', 'Ц': '11100', 
    'Ь': '11101', 'А': '11110', 'Д': '11111', 'М': '01100', 'Р': '01101', 
    'О': '01110', 'Ч': '01111'
}

# 1.4 Кодовий словник Шеннона-Фано
fano_codes = {
    'І': '00', 'В': '010', 'Н': '011', 'Т': '100', 'И': '101',
    'С': '11000', 'Л': '11001', 'П': '11010', 'Е': '11011', 'Ц': '11100',
    'Ь': '11101', 'А': '11110', 'Д': '111110', 'М': '1111110', 
    'Р': '11111110', 'О': '111111110', 'Ч': '111111111'
}

def calculate_metrics(codes_dict):
    # Середня довжина коду L
    l_avg = sum(probs[char] * len(codes_dict[char]) for char in probs)
    # Ефективність за Шенноном
    efficiency = (h / l_avg) * 100
    # Кількість інформації в повідомленні (L * n)
    total_bits = l_avg * n
    return l_avg, efficiency, total_bits

l_huff, eff_huff, bits_huff = calculate_metrics(huffman_codes)
l_fano, eff_fano, bits_fano = calculate_metrics(fano_codes)

print(f"Повідомлення: {name}")
print(f"Кількість символів (n): {n}")
print(f"\n1. Ймовірності літер (pi):\n{formatted_probs}")

print(f"\n2. Ентропія (H) / Нижня межа (Lm): {h:.4f} біт/символ")

print("\n" + "="*40)
print("РЕЗУЛЬТАТИ: МЕТОД ХАФФМАНА")
print("-" * 40)
print(f"Середня довжина (L): {l_huff:.4f} біт/символ")
print(f"Ефективність кодування: {eff_huff:.2f}%")
print(f"Кількість інформації в повідомленні: {bits_huff:.2f} біт")

print("\n" + "="*40)
print("РЕЗУЛЬТАТИ: МЕТОД ШЕННОНА-ФАНО")
print("-" * 40)
print(f"Середня довжина (L): {l_fano:.4f} біт/символ")
print(f"Ефективність кодування: {eff_fano:.2f}%")
print(f"Кількість інформації в повідомленні: {bits_fano:.2f} біт")