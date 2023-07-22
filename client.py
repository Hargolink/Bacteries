import socket
import math
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование

sock.connect(("localhost", 15200))  # Подключаемся к server через ip и порт
pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)#Находим центр экрана
old = (0, 0)
radius = 50
dis = pygame.display.set_mode((WIDTH, HEIGHT))# Задаём размеры окошка
pygame.display.set_caption("Бактерии") # Задаём имя окошка
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
    data = sock.recv(1024).decode()
    print("Получил", data)
    dis.fill('gray')
    pygame.draw.circle(dis, 'red', CC, radius)
    pygame.display.update()
    #sock.send("Привет".encode())
    # Мы отправляем команду и кодируем

pygame.quit()



