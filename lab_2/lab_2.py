import cv2 
import numpy as np 

def calculate_entropy(image): 
    # Обчислюємо гістограму (256 рівнів для 8-бітного зображення)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]).ravel() 
    prob = hist / hist.sum() 
    prob = prob[prob > 0] 
    entropy = -np.sum(prob * np.log2(prob)) 
    return entropy 

def quantize_image(image, levels): 
    # Рівномірне квантування: приводимо до діапазону [0, levels-1], 
    # округлюємо і повертаємо назад у [0, 255]
    factor = 255.0 / (levels - 1) 
    quantized = np.round(image / 255.0 * (levels - 1)) * factor 
    return quantized.astype(np.uint8) 

def calculate_relative_entropy(img_p, img_q): 
    # Для відносної ентропії важливо порівнювати розподіли інтенсивностей
    hist_p = cv2.calcHist([img_p], [0], None, [256], [0, 256]).ravel() 
    hist_q = cv2.calcHist([img_q], [0], None, [256], [0, 256]).ravel() 
     
    p = hist_p / hist_p.sum() 
    q = hist_q / hist_q.sum() 
     
    epsilon = np.finfo(float).eps 
    # Замінюємо 0 на epsilon, щоб уникнути ділення на 0 та log(0)
    p_safe = np.where(p == 0, epsilon, p) 
    q_safe = np.where(q == 0, epsilon, q) 
     
    kl_div = np.sum(p * np.log2(p_safe / q_safe)) 
    return kl_div 

if __name__ == "__main__": 
    file_name = 'lab_2\Blake_bloom.jpg' 
    img_orig = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) 
     
    if img_orig is None: 
        print(f"Помилка: файл {file_name} не знайдено.")
        exit()

    # 1 & 2. Оригінал та його ентропія
    print(f"1. Ентропія оригіналу: {calculate_entropy(img_orig):.4f} біт/піксель\n") 

    # 3. Дискретизація
    img_d2 = img_orig[::2, ::2] 
    img_d4 = img_orig[::4, ::4] 
    
    # Словник для ітерації по всіх випадках (Пункт 4, 5, 7)
    test_cases = {
        'Оригінальне': img_orig,
        'Дискретизація (крок 2)': img_d2,
        'Дискретизація (крок 4)': img_d4
    }
    
    quant_levels = [8, 16, 64]

    print("--- Результати для всіх комбінацій (Пункт 4, 5, 7) ---")
    for name, current_img in test_cases.items():
        print(f"\n>>> Обробка: {name} (Розмір: {current_img.shape})")
        
        # Ентропія до квантування
        ent_before = calculate_entropy(current_img)
        print(f"    Базова ентропія: {ent_before:.4f}")
        
        for L in quant_levels:
            # 4. Рівномірне квантування
            img_q = quantize_image(current_img, L)
            
            # 5. Ентропія після квантування
            ent_after = calculate_entropy(img_q)
            
            # 7. Відносна ентропія порівняно з неквантованим варіантом
            rel_ent = calculate_relative_entropy(current_img, img_q)
            
            print(f"    Рівнів: {L:2d} | Ентропія: {ent_after:.4f} | Відносна: {rel_ent:.4f}")

    # 6. Відновлення методом найближчого сусіда
    h, w = img_orig.shape 
    img_d2_restored = cv2.resize(img_d2, (w, h), interpolation=cv2.INTER_NEAREST) 
    img_d4_restored = cv2.resize(img_d4, (w, h), interpolation=cv2.INTER_NEAREST) 

    # Збереження результатів для перевірки
    cv2.imwrite('restored_step2.png', img_d2_restored)
    cv2.imwrite('restored_step4.png', img_d4_restored)
    
    print("\n6. Зображення відновлено та збережено ('restored_step2.png', 'restored_step4.png').")
    print("Програма завершена успішно.")