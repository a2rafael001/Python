import overpy
import xml.etree.ElementTree as ET
import time
from collections import Counter

# Функция для чтения координат из файла OSM
def read_coordinates_from_osm(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Ищем элементы <node>, содержащие координаты
        nodes = []
        for node in root.findall("node"):
            lat = node.get("lat")
            lon = node.get("lon")
            if lat and lon:
                nodes.append((float(lat), float(lon)))
        return nodes
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []

# Пути к файлам OSM
file_paths = [
    r"C:\Users\123\Desktop\3_kurs\pyton\osm\2.osm",
    r"C:\Users\123\Desktop\3_kurs\pyton\osm\2 - 2.osm"
]

# Чтение координат из всех файлов
all_coordinates = []
for file_path in file_paths:
    coordinates = read_coordinates_from_osm(file_path)
    if coordinates:
        all_coordinates.extend(coordinates)

if not all_coordinates:
    print("Не удалось получить координаты из файлов OSM.")
    exit()

# Подключаемся к API Overpass
api = overpy.Overpass()

# Формируем запрос к Overpass API на основе координат
min_lat = min(coord[0] for coord in all_coordinates)
max_lat = max(coord[0] for coord in all_coordinates)
min_lon = min(coord[1] for coord in all_coordinates)
max_lon = max(coord[1] for coord in all_coordinates)

query = f"""
[out:json];
node["tourism"="hotel"]({min_lat},{min_lon},{max_lat},{max_lon});
out body;
"""

print("Выполняю запрос к Overpass API...")
start_time = time.time()

try:
    # Выполняем запрос
    result = api.query(query)
    print("Запрос выполнен! Данные успешно получены.")
except Exception as e:
    print(f"Ошибка выполнения запроса: {e}")
    exit()

end_time = time.time()
print(f"Время выполнения запроса: {end_time - start_time:.2f} секунд")

# Список гостиниц
hotels = []
for node in result.nodes:
    name = node.tags.get("name", node.tags.get("name:ru", "Unknown"))  # Название гостиницы
    hotel_type = node.tags.get("tourism", "Unknown")  # Тип объекта
    hotels.append({"name": name, "type": hotel_type})

# Проверяем результат
if not hotels:
    print("Гостиниц не найдено.")
    exit()

# Подсчитываем количество гостиниц каждого типа
type_counts = Counter(hotel["type"] for hotel in hotels)

# Сортируем гостиницы в алфавитном порядке по названию
hotels_sorted = sorted(hotels, key=lambda x: x["name"])

# Выводим результаты
print("\nСтатистика по типам гостиниц:")
for hotel_type, count in type_counts.items():
    print(f"- {hotel_type}: {count}")

print("\nСписок гостиниц в алфавитном порядке:")
for idx, hotel in enumerate(hotels_sorted, start=1):
    print(f"{idx}. {hotel['name']} (Тип: {hotel['type']})")
