import random
import time
import socket
import math
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from russian_names import RussianNames
import pygame


colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato',
         'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange',
         'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow',
         'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green',
         'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen',
         'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue', 'DodgerBlue',
         'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']


MOBS_QUANTITY = 25
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

pygame.init()
WIDTH_ROOM, HEIGHT_ROOM = 4000, 4000
WIDTH_SERVER, HEIGHT_SERVER = 300, 300
FPS = 60
dis = pygame.display.set_mode((WIDTH_SERVER, HEIGHT_SERVER))

pygame.display.set_caption("Сервер")
clock = pygame.time.Clock()

def find(vector):
    first = None
    for num, sign in enumerate(vector):
        if sign == '<':
            first = num
        if sign == '>' and first is not None:
            second = num
            result = map(float, vector[first + 1:second].split(","))
            return result
    return ''

def find_color(info):
    first = None
    for num, sign in enumerate(info):
        if sign == '<':
            first = num
        if sign == '>' and first is not None:
            second = num
            result = info[first + 1:second].split(",")
            return result
    return ''

class Player(Base):
    __tablename__ = 'gamers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=2)
    speed_x = Column(Integer, default=2)
    speed_y = Column(Integer, default=2)
    color = Column(String(250), default='red')
    w_vision = Column(Integer, default=800)
    h_vision = Column(Integer, default=600)  # Добавили размер
    def __init__(self, name, address):
        self.name = name
        self.address = address

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
        self.color = "red"
        self.w_vision = 800
        self.h_vision = 600

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x - self.size <= 0:
            if self.speed_x >= 0:
                self.x += self.speed_x
        elif self.x + self.size >= WIDTH_ROOM:
            if self.speed_x <= 0:
                self.x += self.speed_x
        else:
            self.x += self.speed_x

        if self.y - self.size <= 0:
            if self.speed_y >= 0:
                self.y += self.speed_y
        elif self.y + self.size >= HEIGHT_ROOM:
            if self.speed_y <= 0:
                self.y += self.speed_y
        else:
            self.y += self.speed_y


    def change_speed(self, vector):
        vector = find(vector)
        if vector[0] == 0 and vector[1] == 0:
            self.speed_x = 0
            self.speed_y = 0
        else:
            vector = vector[0] * self.abs_speed, vector[1] * self.abs_speed
            self.speed_x = vector[0], self.speed_y = vector[1]

    def sync(self):
        self.db.size = self.size
        self.db.abs.speed = self.abs.speed
        self.db.speed_x = self.speed_x
        self.db.speed_y = self.speed_y
        self.db.errors = self.errors
        self.db.x = self.x
        self.db.y = self.y
        self.db.color = self.color
        self.db.w_vision = self.w_vision
        self.db.h_vision = self.h_vision
        s.merge(self.db)
        s.commit()

    def load(self):
        self.size = self.db.size
        self.abs.speed = self.db.abs.speed
        self.speed_x = self.db.speed_x
        self.speed_y = self.db.speed_y
        self.errors = self.db.errors
        self.x = self.db.x
        self.y = self.db.y
        self.color = self.db.color
        self.w_vision = self.db.w_vision
        self.h_vision = self.db.h_vision
        s.merge(self.db)
        s.commit()


players = {}
works = True

names = RussianNames(count = MOBS_QUANTITY * 2, patronymic = False, surname = False, rare = True)
names = list(set(names))
for x in range(MOBS_QUANTITY):
    mob1 = Player(names[x], None)
    mob1.color = random.choice(colors)
    mob1.x = random.randint(0, WIDTH_ROOM)
    mob1.y = random.randint(0, HEIGHT_ROOM)
    mob1.speed_x = random.randint(-1, 1)
    mob1.speed_y = random.randint(-1, 1)
    mob1.size = random.randint(10, 100)
    s.add(mob1)
    s.commit()
    locale_mob = LocalPlayer(mob1.id, mob1.name, None, None)
    players[mob1.id] = locale_mob
tick = -1
server_work = True
while server_work:
    clock.tick(FPS)
    tick += 1



while works:
    clock.tick(FPS)
    if tick % 200 == 0:
        try:
            new_socket, addr = main_socket.accept()  # Принимаем входящие
            print('Подключился', addr)
            new_socket.setblocking(False)  # блокируем завершение программы только уже новый сокет
            login = new_socket.recv(1024).decode()
            player = Player("Имя", addr)
            if login.startswith("color"):
                data = find_color(login[6:])
                player.name, player.color = data
            s.merge(player)
            s.commit()
            addr = f'({addr[0]},{addr[1]})'
            data = s.query(Player).filter(Player.address == addr)
            for x in data:
                player = LocalPlayer(x.id, 'Имя', new_socket, addr)
                players[x.id] = player

        except BlockingIOError:  # Ничего не делаем в случае ошибки
            pass

    visible_bacteries = {}
    for x in list(players):
        visible_bacteries[x] = []
    pairs = list(players.items())
    for i in range(0, len(pairs)):
        for j in range(i + 1, len(pairs)):
            hero_1: Player = pairs[i][1]
            hero_2: Player = pairs[j][1]
            dist_x = abs(hero_2.x - hero_1.x)
            dist_y = abs(hero_2.y - hero_1.y)
            if abs(dist_x) <= hero_1.w_vision // 2 + hero_2.size and abs(dist_y) <= hero_1.h_vision // 2 + hero_2.size: # # Нужно доделать зона видимости
                distn = math.sqrt(dist_x ** 2 + dist_y ** 2)
                if distn <= hero_1.size and hero_1 >= 1.1 * hero_2.size:
                    hero_2.size, hero_2.speed_x, hero_2.speed_y = 0, 0, 0
                    if hero_1.address is not None:
                        x_ = str(round(dist_x))
                        y_ = str(round(dist_y))
                        size_ = str(round(hero_2.size))
                        color_ = hero_2.color
                        data = x_ + " " + y_ + " " + size_ + " " + color_
                        visible_bacteries[hero_1.id].append(data)

            if abs(dist_x) <= hero_2.w_vision // 2 + hero_1.size and abs(dist_y) <= hero_2.h_vision // 2 + hero_1.size: # Нужно доделать зона видимости
                distn = math.sqrt(dist_x ** 2 + dist_y ** 2)
                if distn <= hero_2.size and hero_2 >= 1.1 * hero_1.size:
                    hero_1.size, hero_1.speed_x, hero_1.speed_y = 0, 0, 0
                    if hero_2.address is not None:
                        x_ = str(round(-dist_x))
                        y_ = str(round(-dist_y))
                        size_ = str(round(hero_1.size))
                        color_ = hero_1.color
                        data = x_ + " " + y_ + " " + size_ + " " + color_
                        visible_bacteries[hero_2.id].append(data)

        for id in list(players):
            if players[id].errors >= 500 or players[id].size == 0:
                if players[id].sock is not None:
                    players[id].sock.close()
                del players[id]
                s.query(Player).filter(Player.id == id).delete()
                s.commit()

        for id in list(players):
            if players[id].sock is not None:
                visible_bacteries[id] = "<" + ",".join(visible_bacteries[id]) + ">"
                try:
                    players[id].sock.send(visible_bacteries[id].encode())

                except:
                    pass

    for x in list(players):  # Проходимся по списку
        try:
            data = players[x].sock.recv(1024).decode()
            print("Получил", data)
            players[x].change_speed(data)
        except:
            pass
        else:
            if tick % 400 == 0:
                vector = f'{random.randint(-1, 1)}, {random.randint(-1, 1)}'
                players[id].change_speed(vector)

    for x in list(players):
        if players[id].sock is not None:
            try:
                players[x].sock.send("Игра".encode())
            except:
                players[x].sock.close()
                del players[x]
                s.query(Player).filter(Player.id == x).delete()
                s.commit()
                print("Сокет закрыт")
    for event in pygame.event.get():
        if event == pygame.QUIT:
            works = False
    dis.fill('black')
    for id in players:
        player = players[id]
        x = player.x * WIDTH_SERVER // WIDTH_ROOM
        y = player.y * HEIGHT_SERVER // HEIGHT_ROOM
        size = player.size * HEIGHT_SERVER // HEIGHT_ROOM
        pygame.draw.circle(dis, player.color, (x, y), size)
    for id in players:
        player = players[id]
        player.update()

    pygame.display.update()


pygame.quit()

main_socket.close()
s.query(Player).delete()
s.commit()


