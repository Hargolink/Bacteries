import socket
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import math
import pygame

name = ""
color = ""

buffer = 1024
win = tk.Tk()
win.geometry('300x200')
win.title("Авторизация")
style = ttk.Style()
style.theme_use('clam')
name_lbl = tk.Label(win, text="Введите свой никнейм")
name_lbl.pack()
row = tk.Entry(win, width=30, justify="center")
row.pack()
label_col = tk.Label(win, text = "Выберите цвет")
label_col.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato',
         'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange',
         'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow',
         'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green',
         'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen',
         'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue', 'DodgerBlue',
         'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

def login():
    global name
    name = row.get()
    if name and color:
        win.destroy()
        win.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")

def find(vector:str):
    first = None
    for num, sign in enumerate(vector):
        if sign == '<':
            first = num
        if sign == '>' and first is not None:
            second = num
            result = map(float, vector[first + 1:second].split(","))
            return result
    return ''


class Grid:
    def __init__(self, screen, color):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size
        self.color = color

    def update(self, param:list[int]):
        x, y, L = param
        self.size = self.start_size // L
        self.x = -self.size + (-x) % self.size
        self.y = -self.size + (-y) % self.size

    def draw(self):
        for i in range(WIDTH // self.size + 2):
            pygame.draw.line(self.screen, self.color, (self.x + i * self.size + i, 0), (self.x + i * self.size + i, WIDTH), 1)

        for i in range(HEIGHT // self.size + 2):
            pygame.draw.line(self.screen, self.color, (self.y + i * self.size + i, 0), (self.y + i * self.size + i, HEIGHT), 1)

def draw_bacteria(data:list[str]):
    for num, bac in enumerate(data):
        data = bac.split(" ")
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(dis, color, (x, y), size)
        if len(data) > 4:
            draw_text(x, y, size // 2, data[4], color = 'black')

def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox", fieldbackground=color, background="white")

def draw_text(x, y, radius, text, color):
    font = pygame.font.Font(None, radius)
    text = font.render(text, True, color)
    rect = text.get_rect(center = (x, y))
    dis.blit(text, rect)

combo = ttk.Combobox(win, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()

but = tk.Button(win, text='Зайти в игру', command=login)
but.pack()
win.mainloop()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование

sock.connect(("localhost", 1000))  # Подключаемся к server через ip и порт
sock.send(("color:<" + name + "," + color + ">").encode())
pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)#Находим центр экрана
old = (0, 0)
radius = 50
dis = pygame.display.set_mode((WIDTH, HEIGHT))# Задаём размеры окошка
pygame.display.set_caption("Бактерии") # Задаём имя окошка
grid = Grid(dis, "red")
run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()# Узнаём к координаты мышки
            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0]**2 + vector[1]**2)
            vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = 0, 0
            if vector != old:# сравниваем нынешние координаты и старые
                old = vector# Заменяем координаты
                msg = f"<{vector[0]},{vector[1]}>"# В msg хранятся новые координаты
                sock.send(msg.encode())
    data = sock.recv(buffer).decode()
    data = find(data).split(",")
    print("Получил", data)
    #print(data)
    dis.fill('gray')
    pygame.draw.circle(dis, color, CC, radius)
    draw_text(CC[0], CC[1], radius // 2, name, color = 'black')
    if data != [""]:
        param = list(map(int, data[0].split(" ")))
        radius = param[0]
        grid.update(param[1:])
        grid.draw()
        draw_bacteria(data[1:])
    pygame.display.update()
    pygame.display.update()
    pygame.display.update()
    sock.send("Привет".encode())
    # Мы отправляем команду и кодируем

pygame.quit()



