import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование

sock.connect(("localhost", 15200))#Подключаемся к server через ip и порт
while True:

    sock.send("Привет".encode())#Мы отправляем команду и кодируем





