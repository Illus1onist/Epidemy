import math
import pygame

import random

FPS = 30

cost = 100  # стоимость прокачки обычных эволюций
mutation_cost = 2000  # стоимость мутации

# параметры вируса
mutation = False
letal = False
zaraz = False
imun = False
lab = False
score = 0  # счёт

RED = 0xFF0000
LIGHTRED = 0xFF4C5B
DARKBLUE = 0x0000FF
BLUE = 0x42AAFF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
ORANGE = 0xFFA500
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, DARKBLUE, YELLOW, GREEN, MAGENTA, CYAN, ORANGE]

WIDTH = 1500
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
samolet_infected = pygame.image.load('samolet.png').convert_alpha()
samolet_common = pygame.image.load('samolet1.png').convert_alpha()

TK = 1.2
frequencyofvirus = 1.6
startproc = 0.03

Rusual = 5


class Scale:
    """
    Класс шкал уровней эволюций вируса
    screen1 - поверхность отображения
    x, y - координаты
    width, height - ширина и высота соответственно
    color - цвет заполнения
    lvl - величина заполнения
    """

    def __init__(self, screen1: pygame.Surface, x, y, width, height, color, lvl):
        self.screen = screen1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface((self.width, self.height))
        self.lvl = lvl

    def draw(self):
        """
        Функция отрисовки шкалы
        """
        pygame.draw.rect(self.screen, self.color, (self.x + 2, self.y + self.height - (self.height / 10) * self.lvl + 2,
                                                   self.width - 5, (self.height / 10) * self.lvl - 4))
        for i in range(0, 10):
            pygame.draw.rect(self.screen, BLACK,
                             (self.x, self.y + i * (self.height / 10),
                              self.width, self.height / 10), 4)


class Country:
    """
    Класс стран
    name - название страны
    Cities - список городов этой страны
    """

    def __init__(self, name):
        self.name = name
        self.Cities = []


widthramki = 350  # ширина рамки
heightramki = 350  # высота рамки
# координаты рамки
coordxramki = 1125
coordyramki = 25
# ширина и высота кнопки
buttonwidth = 50
buttonheight = 50


class Plane:
    """
    Класс самолётов
    x, y - координаты самолёта
    end_x, end_y - координаты места прибытия
    end_country, end_city - страна и город прибытия
    velocity - скорость передвижения самолета
    velocity_x, velocity_y - проекции скорости движения на координатные оси
    infected - параметр, определяющий наличие заражённого юнита на борту
    image - сам самолет, отображаемый на экране (красный, если infected = True, синий, если infected = False)
    """

    def __init__(self, screen1: pygame.Surface, x, y, end_x, end_y, velocity, infected, end_country, end_city):
        self.screen = screen1
        self.x = x
        self.y = y
        self.end_x = end_x
        self.end_y = end_y
        self.end_country = end_country
        self.end_city = end_city
        self.velocity = velocity
        r = math.sqrt((self.end_x - x) ** 2 + (self.end_y - y) ** 2)
        self.velocity_x = velocity * ((end_x - x) / r)
        self.velocity_y = velocity * ((end_y - y) / r)
        rotate = math.degrees(math.atan2(y - end_y, end_x - x))
        self.infected = infected
        if self.infected:
            self.image = pygame.transform.rotate(samolet_infected, rotate)
        else:
            self.image = pygame.transform.rotate(samolet_common, rotate)

    def move(self):
        """
        Функция, описывающая движение самолёта
        """
        self.x += self.velocity_x
        self.y += self.velocity_y


class City:
    """
    Класс, описывающий города
    x, y - координаты верхнего левого угла иконки
    xo, yo - координаты левого нижнего угла иконки
    N - число людей, населяющих этот город
    number_of_infected и number_of_deceased - количество зараженных и количество умерших соответственно
    Repid - радиус, в котором может заразить больной юнит здорового
    Dpropability - вероятность умереть в каждый день
    propability - вероятность заразиться рядом с больным юнитом
    active - скорость юнитов
    name - название города
    showstatus - показатель, который определяет отображение города. Показывается тот город, который имеет показатель = 1
    , остальные получают показатель = 1
    buttonx, buttony -  положение кнопки города
    timer - время выздоровления юнита в городе
    tourist_probability - величина туризма в городе (увеличивает шанс полета самолеьа в этот город)
    """

    def __init__(self, screen1: pygame.Surface, x, y, xo, yo, n, repid, dpropability, propability, active, name,
                 showstatus, buttonx, buttony, number_of_infected, number_of_deceased, timer, tourist_probability):
        self.screen = screen1
        self.x = x
        self.y = y
        self.xo = xo
        self.yo = yo
        self.N = n
        self.number_of_infected = number_of_infected
        self.number_of_deceased = number_of_deceased
        self.Repid = repid
        self.Dpropability = dpropability
        self.propability = propability
        self.active = active
        self.name = name
        self.showstatus = showstatus
        self.people = []
        self.Buttonx = buttonx
        self.Buttony = buttony
        self.timer = timer
        self.tourist_probability = tourist_probability

    def draw(self):
        """
        Функция отрисовки города (внутри рамки)
        """
        pygame.draw.rect(self.screen, WHITE, (coordxramki, coordyramki, self.xo - self.x, self.yo - self.y))


class Man:
    """
    Класс, опсиывающий юнита
    x, y - координаты юнита
    r - радиус юнита
    live, color - параметр состаяния юнита и связанный с ним цвет соответственно:
        2 - нейтральный юнит (с ним может произойти любое действие), голубой
        1 - зараженный юнит, красный
        0 - переболевший юнит, зелёный
        -1 - погибший юнит, чёрный
    aimcity - город, которому принадлежит этот юнит
    v - скорость юнита
    van - угол движения юнита
    timer - время до выздоровления (если -2, то юнит не болеет)
    """

    def __init__(self, screen1: pygame.Surface, ghoust, x, y, live, city, timer):
        self.screen = screen1
        self.x = x
        self.y = y
        self.r = Rusual
        self.destination = city
        self.v = random.randint(5, 10) * 0.3
        self.van = random.uniform(0, 2 * math.pi)
        self.color = BLUE
        self.live = live
        self.city = city
        self.ghoust = ghoust
        self.waytime = 0
        self.aimcity = city
        if self.live == 2:
            self.timer = -2
        if self.live == 1:
            self.timer = timer

    def move(self):
        """
        Функция, описывающая движение юнитов
        """
        self.van = self.van + random.uniform(-math.pi * 0.1, math.pi * 0.1)
        self.x = self.x + math.cos(self.van) * self.v * self.city.active
        self.y = self.y - math.sin(self.van) * self.v * self.city.active
        if self.x > self.city.xo - self.r:
            self.x = self.city.xo - self.r
            self.van = (random.uniform(math.pi / 2, math.pi * 3 / 2))
        if self.x < self.r + self.city.x:
            self.x = self.r + self.city.x
            self.van = (random.uniform(-math.pi / 2, math.pi / 2))
        if self.y > self.city.yo - self.r:
            self.y = self.city.yo - self.r
            self.van = (random.uniform(0, math.pi))
        if self.y < self.city.y + self.r:
            self.y = self.r + self.city.y
            self.van = (random.uniform(-math.pi, 0))

    def draw(self):
        """
        Функция отрисовки юнита
        """
        pygame.draw.circle(self.screen, self.color, (self.x + (coordxramki - self.city.x),
                                                     self.y + (coordyramki - self.city.y)), self.r)


ramka = pygame.image.load('Ramka.png').convert_alpha()
mapflag = pygame.image.load('metka.png').convert_alpha()
map = pygame.image.load('map.png')
laboratory = pygame.image.load('laboratory.jpeg')
menu_bg = pygame.image.load('virus.png')


def start_game():
    """
    Функция самой игры
    """
    global letal, zaraz, imun, mutation, score
    finished = False
    clock = pygame.time.Clock()
    countries = []
    planes = []
    countries.append(Country('China'))
    countries.append(Country('Russia'))
    countries.append(Country('Netherlands'))
    countries.append(Country('USA'))
    countries.append(Country('Brasilia'))

    countries[0].Cities.append(City(screen, -2000, 0, -2000 + widthramki, heightramki, 150, 21, 0.01, 0.17, 0.3,
                                    'Oohan', 1, 785, 159, 0, 0, 14, 0.005))
    countries[0].Cities.append(City(screen, -1600, 0, -1600 + widthramki, heightramki, 150, 21, 0.01, 0.17, 0.2,
                                    'Beijing', 0, 843, 134, 0, 0, 14, 0.005))
    countries[0].Cities.append(City(screen, -1200, 0, -1200 + widthramki, heightramki, 150, 21, 0.01, 0.17, 0.2,
                                    'Hong-Kong', 0, 898, 185, 0, 0, 14, 0.005))

    countries[1].Cities.append(City(screen, -2000, 400, -2000 + widthramki, 400 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Moscow', 0, 621, 79, 0, 0, 14, 0.005))
    countries[1].Cities.append(City(screen, -1600, 400, -1600 + widthramki, 400 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Chelyabinsk', 0, 748, 72, 0, 0, 14, 0.005))
    countries[1].Cities.append(City(screen, -1200, 400, -1200 + widthramki, 400 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Vladivostok', 0, 933, 98, 0, 0, 14, 0.005))

    countries[2].Cities.append(City(screen, -2000, 800, -2000 + widthramki, 800 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Rotterdam', 0, 528, 90, 0, 0, 14, 0.005))
    countries[2].Cities.append(City(screen, -1600, 800, -1600 + widthramki, 800 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Amsterdam', 0, 484, 123, 0, 0, 14, 0.005))

    countries[3].Cities.append(City(screen, -2000, 1200, -2000 + widthramki, 1200 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Washington', 0, 224, 132, 0, 0, 14, 0.005))
    countries[3].Cities.append(City(screen, -1600, 1200, -1600 + widthramki, 1200 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'New York', 0, 167, 159, 0, 0, 14, 0.005))
    countries[3].Cities.append(City(screen, -1200, 1200, -1200 + widthramki, 1200 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Los Angeles', 0, 81, 149, 0, 0, 14, 0.005))

    countries[4].Cities.append(City(screen, -2000, 1600, -2000 + widthramki, 1600 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Brasilia', 0, 344, 311, 0, 0, 14, 0.005))
    countries[4].Cities.append(City(screen, -1600, 1600, -1600 + widthramki, 1600 + heightramki, 150, 21, 0.015,
                                    0.17, 0.2, 'Rio de Janeiro', 0, 289, 346, 0, 0, 14, 0.005))

    t = 0  # Таймер (работает в течении всей игры)

    """Создание массива юнитов"""
    for k in range(len(countries)):
        for j in range(len(countries[k].Cities)):
            for i in range(countries[k].Cities[j].N):
                if k == 0 and j == 0 and i == 0:
                    live = 1
                else:
                    live = 2
                countries[k].Cities[j].people.append(Man(screen, 0,
                                                         random.uniform(countries[k].Cities[j].x,
                                                                        countries[k].Cities[j].xo),
                                                         random.uniform(countries[k].Cities[j].y,
                                                                        countries[k].Cities[j].yo),
                                                         live, countries[k].Cities[j], countries[k].Cities[j].timer))

    # кнопки эволюции вируса
    letal_b = ButtonGame(170, 80, 1)  # влияет на вероятность смерти
    zaraz_b = ButtonGame(170, 80, 2)  # влияет на вероятность заражения
    imun_b = ButtonGame(170, 80, 3)  # влияет на время выздоровления
    mutation_b = ButtonGame(170, 80, 4)  # мутация

    # Кнопки взаимодействия с лабораторией
    lab_enter = ButtonGame(170, 80, 5)  # Вход в лабораторию
    lab_back = ButtonGame(170, 80, 6)  # Выход из лаборатории

    # Размеры шрифта
    f = pygame.font.Font(None, 60)
    g = pygame.font.Font(None, 40)

    # Шкалы эволюций вируса
    scale_imun = Scale(screen, 790, 100, 70, 500, GREEN, 0)  # Шкала иммунитета
    scale_letal = Scale(screen, 90, 100, 70, 500, MAGENTA, 0)  # Шкала смертоносности
    scale_zaraz = Scale(screen, 440, 100, 70, 500, CYAN, 0)  # Шкала заразности

    # начало цикла основной игры
    while not finished:
        t = t + 1
        screen.fill(WHITE)
        all_infected = 0
        all_deceased = 0
        # Подсчёт умерших и заражённых
        for k in range(len(countries)):
            for j in range(len(countries[k].Cities)):
                all_infected += countries[k].Cities[j].number_of_infected
                all_deceased += countries[k].Cities[j].number_of_deceased

        # Отриовка экрана лаборатории (эволюции вируса).
        if lab:
            screen.blit(laboratory, (0, 0))
            scale_imun.lvl = imun_b.lvl
            scale_imun.draw()
            scale_zaraz.lvl = zaraz_b.lvl
            scale_zaraz.draw()
            scale_letal.lvl = letal_b.lvl
            scale_letal.draw()
            letal_b.draw(50, 650, 'Lethality+1', 'Cost: ' + str(cost), None, 30)
            zaraz_b.draw(400, 650, 'Infection+1', 'Cost: ' + str(cost), None, 30)  # тоже кнопки
            imun_b.draw(750, 650, 'Immune+1', 'Cost: ' + str(cost), None, 30)
            mutation_b.draw(1100, 400, 'Mutation', 'Cost: ' + str(mutation_cost), None, 30)
            lab_back.draw(1100, 650, 'Exit the', 'Lab', None, 30)
        else:
            # Отрисовка юнитов, наименования страны, наименования города,
            # самолетов, рамки, количества зараженных и умерших (в городе),
            # карты мира, кнопки входа в лабораторию.
            screen.blit(map, (0, 0))
            lab_enter.draw(50, 650, 'Enter the', 'Lab', None, 30)
            for k in range(len(countries)):
                for j in range(len(countries[k].Cities)):
                    screen.blit(mapflag, (countries[k].Cities[j].Buttonx, countries[k].Cities[j].Buttony))
                    if countries[k].Cities[j].showstatus == 1:
                        text = f.render(str(countries[k].Cities[j].name), True, (180, 0, 0))
                        screen.blit(text, (1300 - 12 * len(countries[k].Cities[j].name), 385))

                        text = g.render(str(countries[k].name), True, (180, 0, 0))
                        screen.blit(text, (1300 - 8 * len(countries[k].name), 425))

                        text = g.render('infected in the city: ' + str(countries[k].Cities[j].number_of_infected), True,
                                        (180, 0, 0))
                        screen.blit(text, (1100, 465))

                        text = g.render('deceased in the city: ' + str(countries[k].Cities[j].number_of_deceased), True,
                                        (180, 0, 0))
                        screen.blit(text, (1100, 505))

                    for i in range(len(countries[k].Cities[j].people)):
                        if countries[k].Cities[j].people[i].ghoust == 0 and countries[k].Cities[j].people[i].live != -1:
                            countries[k].Cities[j].people[i].move()
                        if countries[k].Cities[j].showstatus == 1:
                            countries[k].Cities[j].people[i].draw()

            screen.blit(ramka, (1110, 10))

            for i in range(len(planes)):
                screen.blit(planes[i].image, (planes[i].x, planes[i].y))

        # Отрисовка общего количества умерших и заболевших, а так же общего счета(левый верхний угол).
        text = g.render('total infected: ' + str(all_infected), True, (180, 0, 0))
        screen.blit(text, (0, 0))

        text = g.render('total deceased: ' + str(all_deceased), True, (180, 0, 0))
        screen.blit(text, (0, 40))

        text = g.render('score: ' + str(score), True, (180, 0, 0))
        screen.blit(text, (0, 80))

        # Передача вируса другим юнитам, увеличение характеристик вируса
        # при нажатой кнопки эволюции
        for i in range(len(countries)):
            for j in range(len(countries[i].Cities)):
                if zaraz:
                    countries[i].Cities[j].propability += 0.04
                if letal:
                    countries[i].Cities[j].Dpropability += 0.04
                if imun:
                    countries[i].Cities[j].timer += 2
                for k in range(len(countries[i].Cities[j].people)):
                    if countries[i].Cities[j].people[k].live == 2:
                        for d in range(len(countries[i].Cities[j].people)):
                            if countries[i].Cities[j].people[d].ghoust == 0 \
                                    and countries[i].Cities[j].people[d].live == 1 \
                                    and (countries[i].Cities[j].people[d].x - countries[i].Cities[j].people[k].x) ** 2 \
                                    + (countries[i].Cities[j].people[d].y - countries[i].Cities[j].people[k].y) ** 2 \
                                    <= countries[i].Cities[j].Repid ** 2 \
                                    and t % (int(FPS / TK / frequencyofvirus)) == 0 \
                                    and random.uniform(0, 1) < countries[i].Cities[j].propability:
                                countries[i].Cities[j].people[k].live = 1
                                countries[i].Cities[j].people[k].timer = countries[i].Cities[j].timer
                                score += 10

        # Вылет самолетов и определние наличия на борту зараженного юнита
        for i in range(len(countries)):
            for j in range(len(countries[i].Cities)):
                for k in range(len(countries)):
                    for d in range(len(countries[k].Cities)):
                        if random.uniform(0, 1) < countries[k].Cities[d].tourist_probability \
                                and countries[i].Cities[j] != countries[k].Cities[d] \
                                and t % (int(FPS / TK)) == 0:
                            if random.uniform(0, 1) < countries[i].Cities[j].number_of_infected * 0.005:
                                planes.append(Plane(screen, countries[i].Cities[j].Buttonx,
                                                    countries[i].Cities[j].Buttony, countries[k].Cities[d].Buttonx,
                                                    countries[k].Cities[d].Buttony, 5, True, k, d))
                            else:
                                planes.append(Plane(screen, countries[i].Cities[j].Buttonx,
                                                    countries[i].Cities[j].Buttony, countries[k].Cities[d].Buttonx,
                                                    countries[k].Cities[d].Buttony, 5, False, k, d))

        # Движение самолетов
        for i in range(len(planes)):
            planes[i].move()

        # Приземление самолетов и высадка зараженных юнитов, если таковые имеются
        for i in planes:
            if (i.x - i.end_x) ** 2 + (i.y - i.end_y) ** 2 <= 50:
                if i.infected:
                    k = i.end_country
                    d = i.end_city
                    j = random.randint(0, countries[k].Cities[d].N)
                    countries[k].Cities[d].people[j].live = 1
                    countries[k].Cities[d].people[j].timer = countries[k].Cities[d].timer
                    score += 10
                planes.remove(i)

        # Уменьшение значение таймера болезни у юнитов
        for i in range(len(countries)):
            for j in range(len(countries[i].Cities)):
                for k in range(len(countries[i].Cities[j].people)):
                    if countries[i].Cities[j].people[k].live == 1 and t % (int(FPS / TK)) == 0:
                        countries[i].Cities[j].people[k].timer -= 1

        # Определение состояния юнита после болезни(выздоравливает или умерает)
        for i in range(len(countries)):
            for j in range(len(countries[i].Cities)):
                for k in range(len(countries[i].Cities[j].people)):
                    if countries[i].Cities[j].people[k].live == 1 and t % (int(FPS) / TK) == 0:
                        if random.uniform(0, 1) < countries[i].Cities[j].Dpropability:
                            countries[i].Cities[j].people[k].live = -1
                            score += 30
                    if countries[i].Cities[j].people[k].timer == -1 and countries[i].Cities[j].people[k].live == 1 \
                            and t % (int(FPS) / TK) == 0:
                        if random.uniform(0, 1) < countries[i].Cities[j].Dpropability:
                            countries[i].Cities[j].people[k].live = -1
                            score += 30
                        else:
                            countries[i].Cities[j].people[k].live = 0

        # Присвоение юнитам цвета в соответствии с их состоянием
        for i in range(len(countries)):
            for j in range(len(countries[i].Cities)):
                countries[i].Cities[j].number_of_deceased = 0
                countries[i].Cities[j].number_of_infected = 0
                for k in range(len(countries[i].Cities[j].people)):
                    if countries[i].Cities[j].people[k].live == 1:
                        countries[i].Cities[j].number_of_infected += 1
                        countries[i].Cities[j].people[k].color = RED
                    if countries[i].Cities[j].people[k].live == 0:
                        if mutation:
                            countries[i].Cities[j].people[k].live = 2
                        else:
                            countries[i].Cities[j].people[k].color = GREEN
                    if countries[i].Cities[j].people[k].live == -1:
                        countries[i].Cities[j].number_of_deceased += 1
                        countries[i].Cities[j].people[k].color = BLACK
                    if countries[i].Cities[j].people[k].live == 2:
                        countries[i].Cities[j].people[k].color = BLUE
        # Обновление эволюции
        mutation = False
        imun = False
        letal = False
        zaraz = False

        pygame.display.update()

        # Оператор для кнопок
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    for i in range(len(countries)):
                        help = 0
                        for j in range(len(countries[i].Cities)):
                            if countries[i].Cities[j].Buttonx < event.pos[0] < \
                                    countries[i].Cities[j].Buttonx + buttonwidth and countries[i].Cities[j].Buttony < \
                                    event.pos[1] < countries[i].Cities[j].Buttony + buttonheight:
                                for a in range(len(countries)):
                                    for b in range(len(countries[a].Cities)):
                                        countries[a].Cities[b].showstatus = 0
                                countries[i].Cities[j].showstatus = 1
                                print(i, j)
                                help = 1
                                break
                        if help == 1:
                            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    for i in range(len(countries)):
                        help = 0
                        for j in range(len(countries[i].Cities)):
                            if countries[i].Cities[j].Buttonx < event.pos[0] < \
                                    countries[i].Cities[j].Buttonx + buttonwidth and countries[i].Cities[j].Buttony < \
                                    event.pos[1] < countries[i].Cities[j].Buttony + buttonheight:
                                for a in range(len(countries)):
                                    for b in range(len(countries[a].Cities)):
                                        countries[a].Cities[b].showstatus = 0
                                countries[i].Cities[j].showstatus = 1
                                print(i, j)
                                help = 1
                                break
                        if help == 1:
                            break

        clock.tick(FPS)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='etna.otf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class ButtonMenu:
    """
    Класс кнопок главного меню
    width и height - ширина и высота соответственно
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=50):
        """
        Функция отрисоки кнопки и выполнения присвоенной ей команды
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                button_sound = pygame.mixer.Sound('button2.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


class ButtonGame:
    """
    Класс игровых кнопок
    width и height - ширина и высота соответственно
    type - тип кнопки (в зависимости от этого параметра кнопка выполняет ту или иную функцию)
    inactive_color - цвет ненажатой кнопки
    active_color - цвет нажатой кнопки
    """

    def __init__(self, width, height, type):
        self.width = width
        self.height = height
        self.type = type
        self.inactive_color = (205, 41, 144)
        self.active_color = (255, 52, 179)
        self.lvl = 0

    def draw(self, x, y, message1, message2, action=None, font_size=50):
        """
        Функция отрисоки кнопки и выполнения присвоенной ей команды
        """
        global cost, letal, zaraz, imun, mutation, score, mutation_cost, lab
        type = self.type
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height \
                and cost <= score and type < 4 and self.lvl < 10:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                if type == 1:
                    letal = True  # нужно настроить
                if type == 2:
                    zaraz = True  # тоже
                if type == 3:
                    imun = True  # тоже
                score -= cost
                cost += 100
                self.lvl += 1
                button_sound = pygame.mixer.Sound('button2.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and mutation_cost <= score and type == 4:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                mutation = True
                score -= mutation_cost
                mutation_cost += 1000
                button_sound = pygame.mixer.Sound('button2.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and type == 5:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                lab = True
                button_sound = pygame.mixer.Sound('button2.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and type == 6:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                lab = False
                button_sound = pygame.mixer.Sound('button2.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    action()

        print_text(message1, x=x + 10, y=y + 10, font_size=font_size)
        print_text(message2, x=x + (self.width / 2), y=y + 50, font_size=font_size)


def show_menu():
    """
    Функция отображения главного меню и последующего перехода к игре или выхода
    """
    show = True
    start_b = ButtonMenu(300, 70)
    quit_b = ButtonMenu(300, 70)

    '''def show_menu2():
        menu_bg = pygame.image.load('virus.png')
        show2 = True
        primeri_b = Button_menu(300, 70)
        creator_b = Button_menu(300, 70)
        while show2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.blit(menu_bg, (0, 0))
            primeri_b.draw(400, 200, 'New game', start_game, 50)
            creator_b.draw(300, 300, 'Continue game', None, 50)

            pygame.display.update()'''

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_bg, (0, 0))
        start_b.draw(300, 200, 'Start game', start_game, 50)
        quit_b.draw(400, 300, 'Quit game', quit, 50)

        pygame.display.update()


pygame.init()
show_menu()
pygame.quit()
