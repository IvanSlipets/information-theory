import math

def get_parameters(n0):
    """Визначає кількість перевірних розрядів r та загальну довжину n"""
    r = 0
    while (2**r) < (n0 + r + 1):
        r += 1
    n = n0 + r
    return r, n

def is_power_of_two(num):
    """Перевіряє, чи є число ступенем двійки"""
    return (num & (num - 1)) == 0 and num != 0

def display_equations(n, r):
    """Відображає перевірні співвідношення для коду"""
    print("\n" + "="*50)
    print("--- ПЕРЕВІРНІ СПІВВІДНОШЕННЯ ---")
    print("="*50)
    for i in range(r):
        pos = 2**i
        equation = []
        covered_positions = []
        for j in range(1, n + 1):
            if j & pos:
                covered_positions.append(str(j))
                if not is_power_of_two(j):
                    equation.append(f"a_{j}")
        
        print(f"b_{pos} (позиція {pos}) контролює розряди: {', '.join(covered_positions)}")
        print(f"Формула: b_{pos} = " + " ⊕ ".join(equation))
        print("-" * 50)

def encode_hamming(data_bits, n0, r, n):
    """Виконує кодування інформаційного блоку"""
    code = [0] * (n + 1)
    j = 0
    for i in range(1, n + 1):
        if not is_power_of_two(i):
            code[i] = int(data_bits[j])
            j += 1
           
    for i in range(r):
        pos = 2**i
        val = 0
        for k in range(1, n + 1):
            if k & pos:
                val ^= code[k]
        code[pos] = val
    return code

def decode_and_correct(received_code, r, n):
    """Виявляє, виправляє помилку та виводить двійковий синдром"""
    syndrome_val = 0
    syndrome_bits = []
    
    # Обчислюємо результат для кожної контрольної групи
    # Йдемо від старшого контрольного біта до молодшого для коректного двійкового запису
    for i in range(r - 1, -1, -1):
        pos = 2**i
        val = 0
        for k in range(1, n + 1):
            if k & pos:
                val ^= received_code[k]
        
        syndrome_bits.append(str(val))
        if val != 0:
            syndrome_val += pos
           
    # Формуємо двійковий рядок (наприклад, "101")
    syndrome_bin = "".join(syndrome_bits)
    print(f"Розрахований синдром (S{r}...S1): {syndrome_bin} (двійковий)")
    print(f"Синдром у десятковій системі: {syndrome_val}")

    if syndrome_val == 0:
        print("\n[Результат]: Помилок не виявлено.")
    else:
        if syndrome_val <= n:
            print(f"\n[Результат]: Виявлено помилку в розряді №{syndrome_val}")
            received_code[syndrome_val] ^= 1
            print(f"Помилку виправлено. Відновлений код: {''.join(map(str, received_code[1:]))}")
        else:
            print(f"\n[Результат]: Помилка поза межами довжини коду (можливо, декілька помилок).")
       
    decoded_data = ""
    for i in range(1, n + 1):
        if not is_power_of_two(i):
            decoded_data += str(received_code[i])
           
    return decoded_data

def main():
    print("--- Реалізація коду Хемінга ---")
    data = input("Введіть інформаційну послідовність: ").strip()
    
    if not all(bit in '01' for bit in data):
        print("Помилка: введіть тільки 0 та 1")
        return

    r, n = get_parameters(len(data))
    print(f"\nПараметри коду: n0={len(data)}, r={r}, n={n}")
   
    display_equations(n, r)
   
    encoded_list = encode_hamming(data, len(data), r, n)
    encoded_str = "".join(map(str, encoded_list[1:]))
    print(f"\nЗакодована послідовність: {encoded_str}")
   
    try:
        error_pos = int(input(f"\nВведіть номер розряду (1-{n}) для помилки (0 - без помилки): "))
        received_code = encoded_list.copy()
        if 1 <= error_pos <= n:
            received_code[error_pos] ^= 1
            print(f"Послідовність із помилкою:  {''.join(map(str, received_code[1:]))}")
        
        print("\n--- Процес декодування ---")
        decoded_message = decode_and_correct(received_code, r, n)
        print(f"Отримані дані: {decoded_message}")
        
    except ValueError:
        print("Помилка: введіть коректне число.")

if __name__ == "__main__":
    main()