# Преобразование файла в общую структуру
import pandas as pd
from datetime import datetime
# Словарь для замены названий месяцев
MONTHS = {
    "Январь": "January", "Февраль": "February", "Март": "March",
    "Апрель": "April", "Май": "May", "Июнь": "June",
    "Июль": "July", "Август": "August", "Сентябрь": "September",
    "Октябрь": "October", "Ноябрь": "November", "Декабрь": "December"
}

# Переводим русские даты в английский формат
def translate_date(date_str):
    if isinstance(date_str, str):
        for ru_month, en_month in MONTHS.items():
            date_str = date_str.replace(ru_month, en_month)
        return date_str
    return None
# Преобразование числовых строк
def convert_to_float(value):
    if isinstance(value, str):
        if value == "-":  # Пропускаем значения "-"
            return None
        return float(value.replace(',', '.'))
    return value

def prepare_file(file_path):
    data = pd.read_csv(file_path)
    print(f"Список столбцов в {file_path}:")
    print(data.columns.tolist())

    # Обработка дат
    data['Тест начат'] = data['Тест начат'].apply(translate_date)
    data['Тест начат'] = pd.to_datetime(data['Тест начат'], format='%d %B %Y %H:%M', errors='coerce')

    # Приведение к общему формату
    if 'В. 4 /1,00' in data.columns:
        # Умножение на 10 для приведения к /10,00
        for col in ['В. 4 /1,00', 'В. 5 /1,00', 'В. 6 /1,00', 'В. 7 /1,00']:
            data[col] = data[col].apply(convert_to_float) * 10
        # Переименование столбцов
        data.rename(columns={
            'В. 4 /1,00': 'В. 4 /10,00',
            'В. 5 /1,00': 'В. 5 /10,00',
            'В. 6 /1,00': 'В. 6 /10,00',
            'В. 7 /1,00': 'В. 7 /10,00'
        }, inplace=True)

    # Преобразование числовых столбцов
    numeric_columns = [col for col in data.columns if '/10,00' in col or '/100,00' in col]
    for col in numeric_columns:
        data[col] = data[col].apply(convert_to_float)

    # Преобразование "Оценка/10,00" в "Оценка/100,00"
    if 'Оценка/10,00' in data.columns:
        data['Оценка/100,00'] = data['Оценка/10,00'] * 10

    return data


# Объединение и анализ файлов
def analyze_files(file_paths, cutoff_date):
    data_list = [prepare_file(file_path) for file_path in file_paths]
    data = pd.concat(data_list, ignore_index=True)

    # Фильтрация по дате
    cutoff_date = datetime.strptime(cutoff_date, '%d %b %Y %H:%M')
    filtered_data = data[data['Тест начат'] < cutoff_date]
    print(f"Записей после фильтрации по дате: {len(filtered_data)}")

    # Фильтрация по оценке
    filtered_data = filtered_data[filtered_data['Оценка/100,00'] >= 60]
    print(f"Записей после фильтрации по оценке: {len(filtered_data)}")

    # Проверка столбцов для расчётов
    print("Данные для расчёта педагогики:")
    print(filtered_data[['В. 4 /10,00', 'В. 5 /10,00']].head())
    print("Данные для расчёта психологии:")
    print(filtered_data[['В. 6 /10,00', 'В. 7 /10,00']].head())

    # Вычисление средних баллов
    pedagogy_scores = filtered_data[['В. 4 /10,00', 'В. 5 /10,00']].mean(axis=1, skipna=True)
    psychology_scores = filtered_data[['В. 6 /10,00', 'В. 7 /10,00']].mean(axis=1, skipna=True)

    return pedagogy_scores.mean(), psychology_scores.mean()


# Пути к файлам
csv_files = [
    r"C:\Users\123\Desktop\3_kurs\pyton\csv\2 - 1.csv",
    r"C:\Users\123\Desktop\3_kurs\pyton\csv\2 - 2.csv"
]

# Заданная дата для фильтрации
cutoff_date = "12 May 2017 10:09"

# Анализ файлов
avg_pedagogy, avg_psychology = analyze_files(csv_files, cutoff_date)

# Результаты
print(f"Средний балл по педагогике: {avg_pedagogy:.2f}")
print(f"Средний балл по психологии: {avg_psychology:.2f}")
