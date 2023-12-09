from random import randrange as rand
from unit import Unit

class Field:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.matrix = []
        self.generate()

    def is_obstacle(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return True
        return self.matrix[y][x] == '0'

    def generate(self):
        for i in range(self.h):
            self.matrix.append([])
            for j in range(self.w):
                rng = rand(100)
                if rng < 50 :
                    self.matrix[i].append('_') # пустая клетка
                elif rng < 80:
                    self.matrix[i].append('0') # препятствие
                elif rng < 95:
                    self.matrix[i].append('$') # +1 бонус
                else:
                    self.matrix[i].append('*') # -1 hp

    def output(self):
        for row in self.matrix:
            #print(row)
            line =''
            for cell in row:
               line += cell + ' '
            print(line)
    
f = Field(5, 7)
u = Unit('&', 0, 0, f)
print("You have", u.hp, "HP now and", u.scor, "bonuses.\nTo end the game, press E or die!\nYou can also buy a special move in the store.\nPress B to open the stor.")

f.output()
key = ' '
while key != 'e' and u.hp > 0: # e - стопер игры
    key = input("Your move: ")
    u.move(key)
    f.output()
print(" HP:", u.hp, "\n Bonus:", u.scor, "\n The end.") # итожик игры