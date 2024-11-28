вар1
1. Чтение данных: Из файла A считываются параметры N и K, из файла B построчно читаются N высот.
2. Проверка условий: Убеждаемся, что параметры N и K корректны, а данных в файле B достаточно
3. Поиск максимальной суммы: Используя алгоритм скользящего окна, вычисляется участок длиной K с максимальной суммой высот.
4. Вывод результата: Программа возвращает максимальную сумму высот, начало и конец участка дороги (в 1-индексации).

import os

def max_road_assessment(file_a, file_b):
    try:
        # Считываем параметры N и K
        with open(file_a, 'r') as f_a:
            n, k = map(int, f_a.readline().split())

        # Проверка параметров
        if n <= 0 or k <= 0 or k > n:
            raise ValueError("Некорректные значения N и K. Убедитесь, что N > 0, K > 0, и K ≤ N.")

        # Построчное чтение файла B
        max_sum = float('-inf')
        current_sum = 0
        start_index = 0
        max_start = max_end = 0
        window_size = 0

        with open(file_b, 'r') as f_b:
            index = 0  # Индекс текущей позиции
            for line in f_b:
                for height in map(int, line.split()):
                    if index >= n:  # Игнорируем лишние данные
                        break
                    current_sum += height
                    window_size += 1
                    index += 1

                    # Если окно превышает размер K, сдвигаем его
                    if window_size > k:
                        current_sum -= height - k
                        start_index += 1
                        window_size -= 1

                    # Проверяем текущую сумму
                    if window_size == k and current_sum > max_sum:
                        max_sum = current_sum
                        max_start = start_index
                        max_end = index - 1

            # Проверяем, что данных было достаточно
            if index < n:
                raise ValueError(f"Файл B содержит недостаточно данных. Ожидалось {n}, найдено {index}.")

        return max_sum, max_start + 1, max_end + 1  # Переход к 1-индексации
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке: {e}")

# Основная часть программы
if __name__ == "__main__":
    # Пути к файлам
    file_a = input("Введите путь к файлу A: ").strip().strip('"')
    file_b = input("Введите путь к файлу B: ").strip().strip('"')

    # Проверяем существование файлов
    if not os.path.exists(file_a):
        print(f"Файл {file_a} не найден.")
    elif not os.path.exists(file_b):
        print(f"Файл {file_b} не найден.")
    else:
        try:
            print("\nЧтение данных из файлов...")
            result, start, end = max_road_assessment(file_a, file_b)
            print("\nРезультаты вычислений:")
            print("Максимальная оценка участка дороги:", result)
            print(f"Начало участка: {start}, Конец участка: {end}")
        except Exception as e:
            print(f"Ошибка: {e}")

