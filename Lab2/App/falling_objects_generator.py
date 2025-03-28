from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie, QImageReader
from falling_object import FallingObject
import random

def generate_falling_objects(parent):
    falling_objects = []

    for i in range(3):  # Создаем объекты
        label = QLabel(parent)
        label.adjustSize()

        # Создаем QMovie и устанавливаем его для QLabel
        movie = QMovie(f'imgs/object{i + 1}.gif')
        label.setMovie(movie)
        movie.jumpToFrame(0)
        movie.start()

        # Создаем объект QImageReader и устанавливаем путь к изображению
        image_reader = QImageReader(f'imgs/object{i + 1}.gif')
        new_size = image_reader.size()

        # Изменяем размер QLabel
        label.resize(new_size.width(), new_size.height())

        # Дополнительная настройка QLabel
        object_speed = random.randint(1, 3)  # Скорость объекта (рандомно)
        object_frequency = random.uniform(0.1, 1.0)  # Частота появления объекта (рандомно)
        falling_object = FallingObject(label, object_speed, object_frequency, parent)
        falling_objects.append(falling_object)

        # Показываем QLabel
        label.show()

    return falling_objects