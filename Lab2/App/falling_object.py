from PyQt5.QtCore import QTimer
import random

class FallingObject:
    def __init__(self, label, speed, frequency, parent):
        # Инициализация падающего объекта
        self.label = label
        self.speed = speed  # Скорость объекта
        self.frequency = frequency  # Частота появления объекта
        self.fx = -80  # Начальная позиция по X 
        self.fy = -80  # Начальная позиция по Y

    # Метод для перемещения объекта в окне
    def move(self):
        # Если объект не достиг левой границы окна, его координата X уменьшается
        if self.fx > -80:
            self.fx -= self.speed  # Изменение координаты X
            self.label.move(round(self.fx), round(self.fy))  # Перемещение объекта
        else:
            # иначе объект перемещается в начальное положение с новыми случайными координатами Y
            self.fx = self.label.parent().width()
            self.fy = random.randint(0, self.label.parent().height() - self.label.height())
            self.label.move(round(self.fx), round(self.fy))