from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget, QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup, QTabWidget, QTableWidget, QTableWidgetItem, QDialogButtonBox # экранные объекты
from PyQt5.QtGui import QFont, QMovie, QPixmap, QImageReader, QMouseEvent, QIcon
from PyQt5.QtCore import Qt, QTimer, QRect
import sys
from falling_objects_generator import generate_falling_objects
from datetime import datetime
from threading import Thread # В лабе №3 будет этот поток
# Игра galaga в качестве динамически изменяемой коллекции, обрабатываемой потоками.

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = {"W": False, "A": False, "S": False, "D": False}
        self.keys_held_last_tick = {"W": False, "A": False, "S": False, "D": False}
        self.is_game_running = False  # Флаг для отслеживания состояния игры
        self.falling_objects = []

        # Виджет QLabel для отображения фона
        self.background_label = QLabel(self)
        background_image = QPixmap('imgs/pic1.png')
        self.background_label.setPixmap(background_image)
        self.background_label.setScaledContents(True)
        # Надпись
        self.label = QLabel('Press "Start"', self)
        # gif для Юнита
        self.unit = QLabel(self)
        unit = QMovie('imgs/User.gif')
        self.unit.setMovie(unit)
        unit.jumpToFrame(0)
        unit.start()
        # кнопки
        self.button = QPushButton('Start', self) 
        self.click_count = 0
        self.button2 = QPushButton('Exit', self)
        self.setupUI()
        # счетчик
        self.start_time = None
        self.score_label = QLabel(self)
        self.score_label.setGeometry(self.width() - 100, 20, 80, 30)
        
        # ифобокс
        # настройки

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)  # Подключаем обработчик для обновления игры

        # Переменные для плавного движения кнопками
        self.target_x = self.unit.x()
        self.target_y = self.unit.y()

        #th = Thread(target = self.falling_thread)
        #th.start() # запустить поток
        #th.join() - убить поток
        #th.is_alive() - проверить поток на жизнь

# Этот метод настраивает пользовательский интерфейс, устанавливает заголовок окна, 
# размеры, шрифты и обработчики событий для кнопок.
    def setupUI(self):
        # окно
        self.setWindowTitle('My app')
        self.move(0, 0)
        self.setFixedSize(900, 500)
        self.label.move(20, 20)
        # фон
        self.background_label.resize(900, 500)
        # шрифт
        font = QFont()
        font.setFamily('Rubik')
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.adjustSize()
        # кнопки
        self.button.setGeometry(20, 50, 60, 30)
        self.button.clicked.connect(self.toggle_game)
        self.button.adjustSize()
        self.button2.setGeometry(80, 50, 60, 30)
        self.button2.clicked.connect(self.exit_game)
        self.button2.adjustSize()
        # иконка юнита
        image_reader = QImageReader('imgs/User.gif')
        new_size = image_reader.size()
        self.unit.resize(new_size.width() - 20, new_size.height() - 50)
        x_center = (self.width() - self.unit.width()) // 2
        y_center = (self.height() - self.unit.height()) // 2
        self.unit.move(x_center, y_center)

# Метод для обновления положения падающих объектов
    def update_falling_objects(self):
        for obj in self.falling_objects:
            obj.move()
            
# Завершение процесса игры и закрытие приложения
    def exit_game(self):
        print("Exiting the game")
        sys.exit()

# Этот метод обрабатывает событие нажатия клавиш, изменяя координаты объекта unit 
# в соответствии с нажатыми клавишами.
    def keyPressEvent(self, event):
        # Обработка нажатий клавиш с установкой состояния клавиш в массиве boolean
        key = chr(event.key())
        if key in self.keys:
            self.keys[key] = True
        print(key)

    def keyReleaseEvent(self, event):
        # Обработка отпускания клавиш с сбросом состояния клавиш в массиве boolean
        key = chr(event.key())
        if key in self.keys:
            self.keys[key] = False
        print(key)

    def update_position_continuous(self):
        # Плавное движение с зажатыми клавишами
        step = 3  # параметр для управления скоростью

        # Обновляем позицию по горизонтали
        if self.keys["A"]:
            self.target_x = max(0, self.target_x - step)
            print("A")
        if self.keys["D"]:
            self.target_x = min(self.width() - self.unit.width(), self.target_x + step)
            print("D")

        # Обновляем позицию по вертикали
        if self.keys["W"]:
            self.target_y = max(0, self.target_y - step)
            print("W")
        if self.keys["S"]:
            self.target_y = min(self.height() - self.unit.height(), self.target_y + step)
            print("S")

        # Двигаем объект в новую позицию
        self.unit.move(self.target_x, self.target_y)

        # Сохраняем текущее состояние клавиш для следующего тика таймера
        self.keys_held_last_tick = self.keys.copy()

# Этот метод обрабатывает событие нажатия кнопки мыши, перемещая объект unit в 
# координаты, соответствующие положению указателя мыши.
    def mouseMoveEvent(self, event):
        print(event.globalPos())
        mouse_global_pos = event.globalPos()

        new_x = mouse_global_pos.x() - self.unit.width() / 2
        new_y = mouse_global_pos.y() - self.unit.height() / 2

        # Ограничиваем перемещение объекта в пределах окна
        new_x = max(0 - self.unit.width(), min(new_x, self.width() - self.unit.width() / 2))
        new_y = max(0 - self.unit.height(), min(new_y, self.height() - self.unit.height() / 2))

        self.unit.move(round(new_x), round(new_y))

# Метод для переключения состояния игры
    def toggle_game(self):
        if self.is_game_running and self.timer.isActive():
            # Приостановка таймера
            print("Pausing the game")
            self.button.setText('Resume')  # Меняем текст кнопки на "Resume"
            self.timer.stop()  # Используем stop() для приостановки таймера
        elif self.is_game_running and not self.timer.isActive():
            # Если таймер был на паузе, то возобновляем его
            print("Resuming the game")
            self.button.setText('Pause')  # Меняем текст кнопки на "Pause"
            self.timer.start()  # Используем start() для возобновления таймера
        else:
            # Первый старт и активация объектов
            print("Starting the game")
            self.button.setText('Pause')  # Меняем текст кнопки на "Pause"
            # Генерируем падающие объекты
            self.falling_objects = generate_falling_objects(self)
            self.timer.start(5)  # Запускаем таймер обновления игры с интервалом 5 миллисекунд

            self.start_time = datetime.now()
            self.score = 0
            self.update_score_label()

        self.is_game_running = True

    def calculate_score(self):
        end_time = datetime.now()
        elapsed_time = end_time - self.start_time
        self.score = elapsed_time.total_seconds()
        self.update_score_label()

    def update_score_label(self):
        self.score_label.setText(f"Score: {int(self.score)}")

    def check_collision(self):
        unit_rect = QRect(self.unit.x(), self.unit.y(), self.unit.width(), self.unit.height())

        for obj in self.falling_objects:
            obj_rect = QRect(obj.fx+20, obj.fy+30, 20, 30)
            if unit_rect.intersects(obj_rect):
                return True

        return False

# Обновление состояния всех объектов в игре
    def update_game(self):
        #self.update_falling_objects()  # Обновляем падающие объекты
        #self.update_position_continuous()  # Плавное движение с зажатыми клавишами

        if not self.check_collision():
            self.update_falling_objects()
            self.update_position_continuous()
            self.calculate_score()
        else:
            print("Collision detected!")
            self.timer.stop()

# Создается объект QApplication, окно MainWindow, оно отображается, и запускается главный цикл приложения.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
