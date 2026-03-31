import os
import heapq
import math
from collections import Counter

class EntropyCalculator:
    @staticmethod
    def calculate(text):
        # Рахуємо ймовірності появи символів та ентропію за формулою Шеннона
        freqs = Counter(text)
        total = len(text)
        return -sum((f/total) * math.log2(f/total) for f in freqs.values())

    @staticmethod
    def average_code_length(freqs, codes):
        # Обчислюємо математичне сподівання довжини коду
        total = sum(freqs.values())
        return sum((freqs[char] / total) * len(code) for char, code in codes.items())

class ShannonFanoEncoder:
    def __init__(self):
        self.codes = {}

    def _generate_recursive(self, chars_freqs, prefix=""):
        if len(chars_freqs) == 1:
            self.codes[chars_freqs[0][0]] = prefix or "0"
            return

        # Поділ списку на дві частини з максимально близькою сумою частот
        total = sum(f for c, f in chars_freqs)
        acc, split_idx, min_diff = 0, 0, total

        for i in range(len(chars_freqs) - 1):
            acc += chars_freqs[i][1]
            diff = abs(2 * acc - total)
            if diff < min_diff:
                min_diff, split_idx = diff, i
            else:
                break

        self._generate_recursive(chars_freqs[:split_idx + 1], prefix + "0")
        self._generate_recursive(chars_freqs[split_idx + 1:], prefix + "1")

    def get_codes(self, text):
        # Підготовка відсортованих частот для алгоритму
        freqs = sorted(Counter(text).items(), key=lambda x: x[1], reverse=True)
        self.codes = {}
        self._generate_recursive(freqs)
        return self.codes

class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right
    def __lt__(self, other): return self.freq < other.freq

class HuffmanEncoder:
    def _build_tree(self, freqs):
        # Побудова дерева знизу вгору через пріоритетну чергу (купу)
        heap = [HuffmanNode(c, f) for c, f in freqs.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
            heapq.heappush(heap, HuffmanNode(None, n1.freq + n2.freq, n1, n2))
        return heap[0]

    def _generate_codes(self, node, code="", codes=None):
        # Рекурсивний обхід дерева для формування бінарних кодів
        if node.char is not None:
            codes[node.char] = code
            return
        self._generate_codes(node.left, code + "0", codes)
        self._generate_codes(node.right, code + "1", codes)

    def get_codes(self, text):
        if not text: return {}
        root = self._build_tree(Counter(text))
        codes = {}
        self._generate_codes(root, "", codes)
        return codes

def run_analysis(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не знайдено.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    size_bytes = os.path.getsize(file_path)
    freqs = Counter(text)
    entropy = EntropyCalculator.calculate(text)
    
    print(f"--- Аналіз файлу: {file_path} ---")
    print(f"Розмір початкового файлу: {size_bytes} байт")
    print(f"Ентропія (H): {entropy:.4f} біт/символ\n")

    for name, encoder in [("Shannon-Fano", ShannonFanoEncoder()), ("Huffman", HuffmanEncoder())]:
        codes = encoder.get_codes(text)
        avg_len = EntropyCalculator.average_code_length(freqs, codes)
        efficiency = (entropy / avg_len) * 100 if avg_len > 0 else 0
        
        print(f"[{name}]")
        print(f"  Сер. довжина коду (L): {avg_len:.4f} біт")
        print(f"  Ефективність (η): {efficiency:.2f}%")
        print(f"  Надлишковість (L-H): {avg_len - entropy:.4f} біт\n")

if __name__ == "__main__":
    FILE_NAME = "test_data.txt" 
            
    run_analysis(FILE_NAME)