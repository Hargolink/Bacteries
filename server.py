import time
import socket

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование
main_socket.bind(("localhost", 15200))  # ip и порт привязываем к сокету
main_socket.setblocking(False)  # блокируем завершение программы
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных
print("Сокет создался")
players = []
while True:
    try:
        new_socket, addr = main_socket.accept()  # Принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)  # блокируем завершение программы только уже новый сокет
        players.append(new_socket)  # append отвечает за добавление элемента в список
    except BlockingIOError:  # Ничего не делаем в случае ошибки
        pass
    for x in players:  # Проходимся по списку
        try:
            #x.send("LOL".encode())
            data = x.recv(10).decode()  # считываем команды игроков
            print("Получил", data)
        except:

            # players.remove(x)
            # x.close()
            # print("Сокет закрыт")
    for x in players:
        try:
            x.send("LOL".encode())
        except:
            players.remove(x)
            x.close()
            print("Сокет закрыт")

            pass
    time.sleep(1)