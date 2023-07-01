import time
import socket

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)#Отключение пакетирование
main_socket.bind(("localhost", 15200))
main_socket.setblocking(False)
main_socket.listen(5)
print("Сокет создался")
players = []
while True:
    try:
        new_socket, addr = main_socket.accept()#Принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)
        players.append(new_socket)
    except BlockingIOError:
        pass
    for x in players:
        try:
            data = x.recv(1024).decode()
            print("Получил", data)
        except:
            pass




