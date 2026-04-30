from reedsolo import RSCodec

# 1. Задаємо параметри коду (10 перевірочних байтів дозволяють виправити 5 помилок)
rs = RSCodec(10)

# 2. Підготовка даних
# Довжина рядка має бути кратна 8 для коректного перетворення в байти
large_binary_str = "11010101101001011111000001011010" * 4
data_bytes = int(large_binary_str, 2).to_bytes(len(large_binary_str) // 8, byteorder='big')

# Запис вихідних даних у data.txt
with open("data.txt", "wb") as f:
    f.write(data_bytes)
print("Створено файл data.txt")

# 3. Кодування (Результат – файл code.txt)
encoded_bytes = bytearray(rs.encode(data_bytes))

# 4. Спотворення символів (імітуємо 3 помилки)
# Переконуємося, що індекси не виходять за межі довжини повідомлення
if len(encoded_bytes) > 10:
    encoded_bytes[0] = 0x00
    encoded_bytes[5] = 0xFF
    encoded_bytes[10] = 0xAA

with open("code.txt", "wb") as f:
    f.write(encoded_bytes)
print("Закодовано та внесено помилки (code.txt)")

# 5. Декодування файлу code.txt
with open("code.txt", "rb") as f:
    received_bytes = f.read()

try:
    # Відновлюємо дані. Метод повертає: decoded_msg, decoded_full_msg, count
    decoded_msg, decoded_full, count = rs.decode(received_bytes)
    
    # 6. Вивчення інформації в файлі decode.txt
    with open("decode.txt", "wb") as f:
        f.write(decoded_msg)
    print(f"Успішно розкодовано! Виправлено помилок: {count} (decode.txt)")
except Exception as e:
    print(f"Помилка при декодуванні: {e}")