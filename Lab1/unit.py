class Unit:
    def __init__(self, icon, x, y, field):
        self.icon = icon
        self.field = field
        self.x = x #width
        self.y = y #height
        self.scor = 1 #счетчик бонусов
        self.hp = 3 #счетчик здоровья
        self.field.matrix[y][x] = icon # иконка текущего положения

    # меню магазина
    def store(self, y, x):
        choice = ' '
        print("Welcome to the store!\nYou can buy one action for one bonus:\n1. Crush the wall\n2. Rook move\n3. Bishop move\n0. Exit the store\n")
        choice = input("Your choice: ")
        if choice == '1':
            Crush.wall(self, y, x)
        elif choice == '2':
            Rook.move(self, y, x)
        elif choice == '3':
            Bishop.move(self, y, x)
        else:
            return

    #ф-ция передвижения
    def move(self, key):
        x = self.x
        y = self.y
        if key == 'w':
            y -= 1
        elif key == 's':
            y += 1
        elif key == 'a':
            x -= 1
        elif key == 'd':
            x += 1
        elif key == 'b':
            if self.scor > 0:
                Unit.store(self, y, x)
            else:
                print("Not enough bonuses!")
            return
        if self.field.is_obstacle(x, y):
            print('Can not go')
            return
        self.field.matrix[self.y][self.x] = '_'
        self.x = x
        self.y = y
        if self.field.matrix[y][x] == '$':
            self.scor += 1
        if self.field.matrix[y][x] == '*':
            self.hp -= 1
        self.field.matrix[y][x] = self.icon

class Crush(Unit):
    # уничтожение 1 стены без перемещения
    def wall(self, y, x):
        if self.field.matrix[y+1][x] == '0' or self.field.matrix[y-1][x] == '0' or self.field.matrix[y][x+1] == '0' or self.field.matrix[y][x-1] == '0':
            choice = input("Choose the wall: ")
            wall = True
            while wall:
                if choice == 'w' and self.field.matrix[y-1][x] == '0':
                    self.field.matrix[y-1][x] = '_'
                    break
                elif choice == 's' and self.field.matrix[y+1][x] == '0':
                    self.field.matrix[y+1][x] = '_'
                    break
                elif choice == 'a' and self.field.matrix[y][x-1] == '0':
                    self.field.matrix[y][x-1] = '_'
                    break
                elif choice == 'd' and self.field.matrix[y][x+1] == '0':
                    self.field.matrix[y][x+1] = '_'
                    break
                else:
                    choice = input("Choose another side: ")
                self.scor -= 1
        else:
            print("There are no walls here")
            return

class Rook(Unit):
    def fun(self, y, x):
        if self.field.matrix[y][x] == '0': return True
        if self.field.matrix[y][x] == '$': self.scor += 1
        if self.field.matrix[y][x] == '*': self.hp -= 1
        self.field.matrix[y][x] = '_'
        return False
    
    # перемещение как ладья в шахматах (до первого препятствия по вертикали/горизонтали)
    def move(self, y, x):
        print(y, x)
        k = int(input("Choose the height: "))
        l = int(input("Choose the width: "))
        self.field.matrix[y][x] = '_'
        while (y != k and x != l) or (y == k and x == l) or k >= self.field.h or k < 0 or l >= self.field.w or l < 0:
            k = int(input("Choose the height: "))
            l = int(input("Choose the width: "))
        if k > y:
            while y != k:
                y += 1
                if Rook.fun(self, y, x):
                    break
        elif k < y:
            while y != k:
                y -= 1
                if Rook.fun(self, y, x):
                    break
        elif l > x:
            while x != l:
                x += 1
                if Rook.fun(self, y, x):
                    break
        elif l < x:
            while x != l:
                x -= 1
                if Rook.fun(self, y, x):
                    break

        self.field.matrix[y][x] = self.icon
        self.scor -= 1
        self.x = x
        self.y = y

class Bishop(Unit):
    # перемещение как слон в шахматах (до первого препятствия по диагоналям)
    def move(self, y, x):
        print(y, x)
        k = int(input("Choose the height: "))
        l = int(input("Choose the width: "))
        self.field.matrix[y][x] = '_'
        while x == l or y == k or (y == k and x == l) or k >= self.field.h or k < 0 or l >= self.field.w or l < 0 or abs(l - x) != abs(k - y):
            k = int(input("Choose the height: "))
            l = int(input("Choose the width: "))
        if k > y and l > x: # ход в правую нижнюю диагональ
            while y != k and x != l:
                y += 1
                x += 1
                if Rook.fun(self, y, x):
                    break
        elif k < y and l > x: # ход в правую верхнюю диагональ
            while y != k and x != l:
                y -= 1
                x += 1
                if Rook.fun(self, y, x):
                    break
        elif k > y and l < x: # ход в левую нижнюю диагональ
            while y != k and x != l:
                y += 1
                x -= 1
                if Rook.fun(self, y, x):
                    break
        elif k < y and l < x: # ход в левую верхнюю диагональ
            while y != k and x != l:
                y -= 1
                x -= 1
                if Rook.fun(self, y, x):
                    break
        self.field.matrix[y][x] = self.icon
        self.scor -= 1
        self.x = x
        self.y = y