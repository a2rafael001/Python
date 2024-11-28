Создает объекты "Квадрат" и "Пятиугольник":

Пользователь вводит идентификатор, длину стороны и координаты.
Перемещает объекты:

Смещения по 𝑑𝑥
dx и 𝑑𝑦 вводятся с клавиатуры.
Проверяет пересечение:
Выводит, пересекаются ли два объекта после перемещения.
Обрабатывает ошибки:
Проверяет корректность введенных данных (например, положительная длина сторон, формат координат).

import random

# Базовый класс для всех фигур
class Shape:
    def __init__(self, identifier, position=(0, 0)):
        if not isinstance(identifier, str):
            raise TypeError("Идентификатор должен быть строкой.")
        if not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(coord, (int, float)) for coord in position):
            raise ValueError("Позиция должна быть кортежем из двух чисел.")
        
        self.identifier = identifier  # Уникальный идентификатор объекта
        self.position = position  # Положение на плоскости (x, y)
    
    def move(self, dx, dy):
        """Перемещает объект на dx, dy"""
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            raise ValueError("dx и dy должны быть числами.")
        
        self.position = (self.position[0] + dx, self.position[1] + dy)
        print(f"{self.identifier} перемещен в новое положение: {self.position}")

# Класс для квадрата
class Quad(Shape):
    def __init__(self, identifier, side_length, position=(0, 0)):
        if side_length <= 0:
            raise ValueError("Длина стороны квадрата должна быть положительным числом.")
        
        super().__init__(identifier, position)
        self.side_length = side_length  # Длина стороны квадрата

# Класс для пятиугольника
class Pentagon(Shape):
    def __init__(self, identifier, side_length, position=(0, 0)):
        if side_length <= 0:
            raise ValueError("Длина стороны пятиугольника должна быть положительным числом.")
        
        super().__init__(identifier, position)
        self.side_length = side_length  # Длина стороны пятиугольника

# Метод для проверки пересечения двух объектов
def is_intersect(shape1, shape2):
    """Простейшая проверка пересечения двух объектов"""
    if not isinstance(shape1, Shape) or not isinstance(shape2, Shape):
        raise TypeError("Оба объекта должны быть экземплярами класса Shape или его наследников.")
    
    dist_x = abs(shape1.position[0] - shape2.position[0])
    dist_y = abs(shape1.position[1] - shape2.position[1])
    max_distance = (shape1.side_length + shape2.side_length) / 2
    if dist_x <= max_distance and dist_y <= max_distance:
        print(f"{shape1.identifier} и {shape2.identifier} пересекаются.")
        return True
    else:
        print(f"{shape1.identifier} и {shape2.identifier} не пересекаются.")
        return False

# Основной код с вводом данных
if __name__ == "__main__":
    try:
        # Ввод данных для первого объекта (Quad)
        identifier1 = input("Введите идентификатор для квадрата: ")
        side_length1 = float(input("Введите длину стороны квадрата: "))
        position1 = tuple(map(float, input("Введите начальные координаты квадрата (через запятую): ").split(',')))
        quad = Quad(identifier=identifier1, side_length=side_length1, position=position1)

        # Ввод данных для второго объекта (Pentagon)
        identifier2 = input("Введите идентификатор для пятиугольника: ")
        side_length2 = float(input("Введите длину стороны пятиугольника: "))
        position2 = tuple(map(float, input("Введите начальные координаты пятиугольника (через запятую): ").split(',')))
        pentagon = Pentagon(identifier=identifier2, side_length=side_length2, position=position2)

        # Перемещение объектов
        dx1, dy1 = map(float, input("Введите смещение для квадрата (dx, dy через запятую): ").split(','))
        quad.move(dx1, dy1)

        dx2, dy2 = map(float, input("Введите смещение для пятиугольника (dx, dy через запятую): ").split(','))
        pentagon.move(dx2, dy2)

        # Проверка пересечения
        is_intersect(quad, pentagon)
    except (TypeError, ValueError) as e:
        print(f"Ошибка: {e}")


Введите идентификатор для квадрата: Квадрат_1
Введите длину стороны квадрата: 4
Введите начальные координаты квадрата (через запятую): 0,0
Введите идентификатор для пятиугольника: Пятиугольник_1
Введите длину стороны пятиугольника: 5
Введите начальные координаты пятиугольника (через запятую): 3,3
Введите смещение для квадрата (dx, dy через запятую): 2,2
Введите смещение для пятиугольника (dx, dy через запятую): -1,-1
