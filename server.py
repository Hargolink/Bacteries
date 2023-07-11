import time
import socket
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирование
main_socket.bind(("localhost", 15200))  # ip и порт привязываем к сокету
main_socket.setblocking(False)  # блокируем завершение программы
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных
print("Сокет создался")
engine = create_engine("postgresql+psycopg2://postgres:Hargolinkproject@localhost/firstpg")
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()

class Player(Base):
    __tablename__ = 'gamers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=1)
    speed_x = Column(Integer, default=0)
    speed_y = Column(Integer, default=0)
Base.metadata.create_all(engine)

class LocalPlayer:
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0

players = {}

while True:
    try:
        new_socket, addr = main_socket.accept()  # Принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)  # блокируем завершение программы только уже новый сокет
        player = Player("Имя", addr)
        s.merge(player)
        s.commit()
        addr = f'({addr[0]}, {addr[1]})'
        data = s.query(Player).filter(Player.address == addr)
        for x in data:
            player = LocalPlayer(x.id, 'Имя', new_socket, addr)
            players[x.id] = player

    except BlockingIOError:  # Ничего не делаем в случае ошибки
        pass

    for x in list(players):  # Проходимся по списку
        try:
            data = players[x].sock.recv(1024).decode()
            print("Получил", data)
        except:
            pass

    for x in list(players):
        try:
            players[x].sock.send("Игра".encode())
        except:
            players[x].sock.close()
            del players[x]
            s.query(Player).filter(Player.id == x).delete()
            s.commit()
            print("Сокет закрыт")
    time.sleep(1)