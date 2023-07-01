import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование

sock.connect(("localhost", 15200))  # Подключаемся к server через ip и порт
pygame.init()
WIDTH = 800
HEIGHT = 600
dis = pygame.display.set_mode((WIDTH, HEIGHT))# Задаём размеры окошка
pygame.display.set_caption("Бактерии") # Задаём имя окошка
while True:
    sock.send("Привет".encode())  # Мы отправляем команду и кодируем
