import math
import heapq
from collections import Counter
from PIL import Image
import numpy as np
import itertools

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def get_huffman_codes(probabilities):
    """Генерує коди Хаффмана для заданого словника ймовірностей"""
    if not probabilities: return {}
    
    # Будуємо дерево Хаффмана
    heap = [HuffmanNode(char, freq) for char, freq in probabilities.items()]
    heapq.heapify(heap)
    
    if len(heap) == 1:
        return {heap[0].char: "0"}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    huffman_codes = {}
    def generate_codes(node, current_code):
        if node is None: return
        if node.char is not None:
            huffman_codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(heap[0], "")
    return huffman_codes

def process_source(image_path, epsilon=0.01):
    # --- Читання файлу ---
    img = Image.open(image_path).convert('L')
    pixels = np.array(img).flatten()
    
    # --- Знаходимо наші 3 основні смуги ---
    raw_counts = Counter(pixels)
    main_colors = [item[0] for item in raw_counts.most_common(3)]
    
    # --- Прибираємо розмиті пікселі ---
    cleaned_pixels = []
    for p in pixels:
        closest = min(main_colors, key=lambda c: abs(c - p))
        cleaned_pixels.append(closest)
        
    total_pixels = len(cleaned_pixels)
    counts = Counter(cleaned_pixels) # Кількість кожного пікселя
    
    # --- Сформувати список повідомлень і ймовірність їх появи ---
    probabilities = {pixel: count / total_pixels for pixel, count in counts.items()}
    
    # --- 1. Вивід статистики ---
    print(f"Загальна кількість пікселів у зображенні: {total_pixels}")
    print("-" * 30)
    for pixel, count in counts.items():
        print(f"Значення пікселя {pixel}: знайдено {count} разів (P = {probabilities[pixel]:.4f})")
    print("-" * 30)

    # --- Підрахунок кількості інформації у кожному повідомленні ---
    # I = -log2(p)
    print("\nКількість інформації в кожному повідомленні (I):")
    for pixel, p in probabilities.items():
        print(f"I({pixel}) = {-math.log2(p):.4f} біт")

    # --- Рахуємо ентропію H ---
    entropy = -sum(p * math.log2(p) for p in probabilities.values() if p > 0)
    Lm = entropy 
    print(f"\nЕнтропія джерела H (нижня межа Lm) = {entropy:.4f} біт/символ")

    print(f"Нижня оцінка (межа) за Шенноном Lm = {Lm:.4f} біт/повідомлення")
    print("-" * 50)

    # --- Кодування Хаффмана для ОДИНОЧНИХ символів ---
    single_codes = get_huffman_codes(probabilities)
    print("\nКоди Хаффмана для одиночних повідомлень:")
    for pixel, code in single_codes.items():
        print(f"Піксель {pixel}: {code}")

    # --- Кодування блоками для досягнення заданої різниці epsilon ---
    block_size = 0
    diff = float('inf')
    
    print(f"\nПочинаємо блочне кодування (ціль різниця < {epsilon}):")
    
    while diff > epsilon:
        block_size += 1
        
        # Створюємо блоки (комбінації)
        block_probs = {}
        for combo in itertools.product(probabilities.keys(), repeat=block_size):
            p_block = math.prod(probabilities[char] for char in combo)
            if p_block > 0:
                block_probs[combo] = p_block
        
        # Кодування Хаффмана для блоків
        block_codes = get_huffman_codes(block_probs)
        
        # L_block - середня довжина на блок, L - середня на символ
        L_block = sum(block_probs[b] * len(block_codes[b]) for b in block_probs)
        current_L = L_block / block_size
        diff = current_L - Lm
        
        print(f"Крок {block_size}: L = {current_L:.5f} (різниця з Lm: {diff:.5f})")
        

        if block_size > 6: break # Захист від перевантаження

    print(f"\nУмова виконана! При n={block_size} досягнуто L={current_L:.4f}")

process_source("lab_1\lab_1.jpg", epsilon=0.01)
