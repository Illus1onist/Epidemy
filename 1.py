import math
import pygame

import random

FPS = 30

cost = 100  # стоймость прокачки

# параметры вируса
mutation = False
letal = False
zaraz = False
imun = False
score = 0 #счёт

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



TK=1.2
frequencyofvirus=1.6
startproc=0.03

Rusual=5
class country:
    '''
    Класс стран.
    name - название страны.
    Cities - список городов этой страны.
    '''
    def __init__(self,screen:pygame.Surface, x, y,xo,yo,color,Name):
        self.screen = screen
        self.x = x
        self.y = y
        self.xo = xo
        self.yo = yo
        self.color=color
        self.name=Name
        self.Cities=[]
    def draw(self):
        pygame.draw.rect(self.screen,self.color,(self.x,self.y,self.xo-self.x,self.yo-self.y))

widthramki=350
heightramki=350
coordxramki=1125
coordyramki=25

buttonwidth=50
buttonheight=50
class city:
    '''
    Класс, описывающий города.
    x, y - координаты верхнего левого угла иконки.
    xo, yo - координаты левого нижнего угла иконки.
    N - число людей, населяющих этот город.
    number_of_infected и number_of_deceased - количество зараженных и количество умерших соответственно.
    Repid - радиус, в котором может заразить больной юнит здорового.
    Dpropability - вероятность умереть в каждый день.
    propability - вероятность заразиться рядом с больным юнитом.
    active - скорость юнитов.
    name - название города.
    showstatus - показатель, который определяет отображение города. Показывается тот город, который имеет показатель = 1, остальные получают показатель = 1.
    buttonx, buttony -  положение кнопки города.
    timer - время выздоровления юнита в городе.
    '''
    def __init__(self, screen: pygame.Surface, x, y,xo,yo,N,Repid,Dpropability,propability,active,Name,showstatus,buttonx,buttony, number_of_infected, number_of_deceased, timer):
        self.screen = screen
        self.x = x
        self.y = y
        self.xo = xo
        self.yo = yo
        self.N = N
        self.number_of_infected = number_of_infected
        self.number_of_deceased = number_of_deceased
        self.Repid = Repid
        self.Dpropability = Dpropability
        self.propability = propability
        self.active = active
        self.name = Name
        self.showstatus = showstatus
        self.people = []
        self.Buttonx = buttonx
        self.Buttony = buttony
        self.timer = timer
    def draw(self):
        '''
        Функция отрисовки города (внутри рамки)
        '''
        pygame.draw.rect(self.screen,WHITE,(coordxramki,coordyramki,self.xo-self.x,self.yo-self.y))



class man:
    '''
    Класс, опсиывающий юнита.
    x, y - координаты юнита.
    r - радиус юнита.
    live, color - параметр состаяния юнита и связанный с ним цвет соответственно:
        2 - нейтральный юнит (с ним может произойти любое действие), голубой
        1 - зараженный юнит, красный
        0 - переболевший юнит, зелёный
        -1 - погибший юнит, чёрный
    aimcity - город, которому принадлежит этот юнит
    v - скорость юнита
    van - угол движения юнита
    timer - время до выздоровления (если -2, то юнит не болеет)
    '''
    def __init__(self, screen: pygame.Surface, ghoust, x, y, live , city, timer):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = Rusual
        self.destination=city
        self.v = random.randint(5,10)*0.3
        self.van = random.uniform(0,2*math.pi)
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
        '''
        Функция, описывающая движение юнитов.
        '''
        self.van=self.van+random.uniform(-math.pi*0.1,math.pi*0.1)
        self.x = self.x + math.cos(self.van) * self.v * self.city.active
        self.y = self.y - math.sin(self.van) * self.v * self.city.active
        if self.x>self.city.xo-self.r:
            self.x=self.city.xo-self.r
            self.van=(random.uniform(math.pi/2,math.pi*3/2))
        if self.x<self.r+self.city.x:
            self.x=self.r+self.city.x
            self.van=(random.uniform(-math.pi/2,math.pi/2))
        if self.y>self.city.yo-self.r:
            self.y=self.city.yo-self.r
            self.van=(random.uniform(0,math.pi))
        if self.y<self.city.y+self.r:
            self.y=self.r+self.city.y
            self.van=(random.uniform(-math.pi,0))
    def draw(self):
        '''
        Функция отрисовки юнита.
        '''
        pygame.draw.circle(self.screen,self.color,(self.x+(coordxramki-self.city.x),self.y+(coordyramki-self.city.y)),self.r)


def start_game():
    global letal, zaraz, imun, mutation, score
    finished = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    all_infected = 0
    all_deceased = 0
    Countries=[]
    Countries.append(country(screen,1100,350,1425,700,LIGHTRED,'China'))
    Countries.append(country(screen,900,25,1450,300, ORANGE,'Russia'))
    Countries.append(country(screen,590,50,740,350,BLUE,'Netherlands'))
    Countries.append(country(screen,80,170,450,430,DARKBLUE,'USA'))
    Countries.append(country(screen,150,520,500,730,GREEN,'Brasilia'))
    Countries[0].Cities.append(city(screen, -2000, 0, -2000+widthramki, heightramki, 150, 21, 0.01, 0.17, 0.3,'Oohan',1,785,159, 0, 0, 14))
    Countries[0].Cities.append(city(screen, -1600, 0, -1600+widthramki, heightramki, 150, 21, 0.01, 0.17, 0.2,'Beijin',0,843,134, 0, 0, 14))
    Countries[0].Cities.append(city(screen, -1200, 0, -1200+widthramki, heightramki, 150, 21, 0.01, 0.17, 0.2,'Hong-Kong',0,898,185, 0, 0, 14))

    Countries[1].Cities.append(city(screen, -2000, 400, -2000+widthramki, 400+heightramki, 150, 21, 0.015, 0.17, 0.2,'Moscow',0,621,79, 0, 0, 14))
    Countries[1].Cities.append(city(screen, -1600, 400, -1600+widthramki, 400+heightramki, 150, 21, 0.015, 0.17, 0.2,'Chelyabinsk',0,748,72, 0, 0, 14))
    Countries[1].Cities.append(city(screen, -1200, 400, -1200+widthramki, 400+heightramki, 150, 21, 0.015, 0.17, 0.2,'Vladivstok',0,933,98, 0, 0, 14))

    Countries[2].Cities.append(city(screen, -2000, 800, -2000+widthramki, 800+heightramki, 150, 21, 0.015, 0.17, 0.2,'Rotterdam',0,528,90, 0, 0, 14))
    Countries[2].Cities.append(city(screen, -1600, 800, -1600+widthramki, 800+heightramki, 150, 21, 0.015, 0.17, 0.2,'Amsterdam',0,484,123, 0, 0, 14))

    Countries[3].Cities.append(city(screen, -2000, 1200, -2000+widthramki, 1200+heightramki, 150, 21, 0.015, 0.17, 0.2,'Washington',0,224,132, 0, 0, 14))
    Countries[3].Cities.append(city(screen, -1600, 1200, -1600+widthramki, 1200+heightramki, 150, 21, 0.015, 0.17, 0.2,'New York',0,167,159, 0, 0, 14))
    Countries[3].Cities.append(city(screen, -1200, 1200, -1200+widthramki, 1200+heightramki, 150, 21, 0.015, 0.17, 0.2,'Los Anjeles',0,81,149, 0, 0, 14))

    Countries[4].Cities.append(city(screen, -2000, 1600, -2000+widthramki, 1600+heightramki, 150, 21, 0.015, 0.17, 0.2,'Brasilia',0,344,311, 0, 0, 14))
    Countries[4].Cities.append(city(screen, -1600, 1600, -1600+widthramki, 1600+heightramki, 150, 21, 0.015, 0.17, 0.2,'Rio de Janeiro',0,289,346, 0, 0, 14))

    t=0 # Таймер (работает в течении всей игры)

    #Создание массива юнитов
    for k in range (len(Countries)):
        for j in range (len(Countries[k].Cities)):
            for i in range (Countries[k].Cities[j].N):
                if k==0 and j==0 and i==0:
                    live=1
                else:
                    live=2
                Countries[k].Cities[j].people.append(man(screen,0,random.uniform(Countries[k].Cities[j].x,Countries[k].Cities[j].xo),random.uniform(Countries[k].Cities[j].y,Countries[k].Cities[j].yo),live,Countries[k].Cities[j], Countries[k].Cities[j].timer))

    # кнопки эволюции вируса
    letal_b = Button_game(170, 80, 1) #влияет на вероятность смерти
    zaraz_b = Button_game(170, 80, 2) #влияет на вероятность заражения
    imun_b = Button_game(170, 80, 3) #влияет на время выздоровления
    mutation_b = Button_game(170, 80, 4)

    #начало цикла основной игры
    while not finished:
        t=t+1
        screen.fill(WHITE)
        #отрисовка карты и кнопок эволюции вируса на экран
        map = pygame.image.load('map.png')
        screen.blit(map, (0, 0))
        print(mutation)
        letal_b.draw(50, 650, 'Lethality+1', str(cost), None, 30)
        zaraz_b.draw(400, 650, 'Infection+1', str(cost),  None, 30)   # тоже кнопки
        imun_b.draw(750, 650, 'Immune+1', str(cost),  None, 30)
        mutation_b.draw(1100, 650, 'Mutation', str(cost),  None, 30)
        #Подсчёт умерших и заражённых. Отрисовка юнитов, наименования страны, наименования города, количества зараженных и умерших.
        all_infected = 0
        all_deceased = 0
        for k in range(len(Countries)):
            for j in range (len(Countries[k].Cities)):
                all_infected += Countries[k].Cities[j].number_of_infected
                all_deceased += Countries[k].Cities[j].number_of_deceased
                if zaraz:
                    Countries[k].Cities[j].propability += 0.02
                if letal:
                    Countries[k].Cities[j].Dpropability += 0.02
                if imun:
                    Countries[k].Cities[j].timer += 1
                if Countries[k].Cities[j].showstatus==1:
                    f = pygame.font.Font(None, 60)
                    text = f.render(str(Countries[k].Cities[j].name), True, (180, 0, 0))
                    screen.blit(text, (1300-12*len(Countries[k].Cities[j].name), 385))

                    g = pygame.font.Font(None, 40)
                    text = g.render(str(Countries[k].name), True, (180, 0, 0))
                    screen.blit(text, (1300-8*len(Countries[k].name),425))

                    text = g.render('infected in the city: '+str(Countries[k].Cities[j].number_of_infected), True, (180, 0, 0))
                    screen.blit(text, (1100,465))

                    text = g.render('deceased in the city: '+str(Countries[k].Cities[j].number_of_deceased), True, (180, 0, 0))
                    screen.blit(text, (1100,505))

                    text = g.render('total infected: '+str(all_infected), True, (180, 0, 0))
                    screen.blit(text, (0, 0))
                    
                    text = g.render('total deceased: '+str(all_deceased), True, (180, 0, 0))
                    screen.blit(text, (0, 40))

                    text = g.render('score: '+str(score), True, (180, 0, 0))
                    screen.blit(text, (0, 80))

                for i in range (len(Countries[k].Cities[j].people)):
                    if Countries[k].Cities[j].people[i].ghoust==0 and Countries[k].Cities[j].people[i].live!=-1:
                        Countries[k].Cities[j].people[i].move()
                    if Countries[k].Cities[j].showstatus == 1:
                        Countries[k].Cities[j].people[i].draw()
        #drawing ramka above and metki
        ramka = pygame.image.load('Ramka.png').convert_alpha()
        screen.blit(ramka, (1110, 10))
        mapflag = pygame.image.load('metka.png').convert_alpha()


        #Передача вируса другим юнитам
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                screen.blit(mapflag, (Countries[i].Cities[j].Buttonx,Countries[i].Cities[j].Buttony))
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live == 2:
                        for l in range(len(Countries[i].Cities[j].people)):
                            if Countries[i].Cities[j].people[l].ghoust == 0 and Countries[i].Cities[j].people[l].live == 1 and (Countries[i].Cities[j].people[l].x - Countries[i].Cities[j].people[k].x) ** 2 + (Countries[i].Cities[j].people[l].y - Countries[i].Cities[j].people[k].y) ** 2 <= Countries[i].Cities[j].Repid**2 and t % (int(FPS / TK / frequencyofvirus)) == 0 and random.uniform(0, 1) < Countries[i].Cities[j].propability:
                                Countries[i].Cities[j].people[k].live = 1
                                Countries[i].Cities[j].people[k].timer = Countries[i].Cities[j].timer
                                score += 10

        #Уменьшение значение таймера болезни у юнитов
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live==1  and t%(int(FPS/TK))==0:
                        Countries[i].Cities[j].people[k].timer -= 1


        #Определение состояния юнита после болезни(выздоравливает или умерает)
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live == 1 and t % (int(FPS) / TK) == 0:
                        if random.uniform(0,1)<Countries[i].Cities[j].Dpropability:
                            Countries[i].Cities[j].people[k].live = -1
                            score += 30
                    if Countries[i].Cities[j].people[k].timer==-1 and Countries[i].Cities[j].people[k].live==1 and t%(int(FPS)/TK)==0:
                        if random.uniform(0,1)<Countries[i].Cities[j].Dpropability:
                            Countries[i].Cities[j].people[k].live = -1
                            score += 30
                        else:
                            Countries[i].Cities[j].people[k].live = 0



        #Присвоение юнитам цвета в соответствии с их состоянием
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                Countries[i].Cities[j].number_of_deceased = 0
                Countries[i].Cities[j].number_of_infected = 0
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live==1:
                        Countries[i].Cities[j].number_of_infected += 1
                        Countries[i].Cities[j].people[k].color=RED
                    if Countries[i].Cities[j].people[k].live==0:
                        if mutation:
                            Countries[i].Cities[j].people[k].live=2
                        else:
                            Countries[i].Cities[j].people[k].color = GREEN
                    if Countries[i].Cities[j].people[k].live==-1:
                        Countries[i].Cities[j].number_of_deceased += 1
                        Countries[i].Cities[j].people[k].color = BLACK
                    if Countries[i].Cities[j].people[k].live==2:
                        Countries[i].Cities[j].people[k].color = BLUE
        mutation = False
        imun = False
        letal = False
        zaraz = False

        pygame.display.update()

        #operator for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    print(event.pos[0],event.pos[1])
                    for i in range(len(Countries)):
                        help=0
                        for j in range(len(Countries[i].Cities)):
                            if event.pos[0]>Countries[i].Cities[j].Buttonx and event.pos[0]<Countries[i].Cities[j].Buttonx+buttonwidth and event.pos[1]>Countries[i].Cities[j].Buttony and event.pos[1]<Countries[i].Cities[j].Buttony+buttonheight:
                                for a in range(len(Countries)):
                                    for b in range(len(Countries[a].Cities)):
                                        Countries[a].Cities[b].showstatus = 0
                                Countries[i].Cities[j].showstatus = 1
                                print(i,j)
                                help=1
                                break
                        if help==1:
                            break

        clock.tick(FPS)



screen = pygame.display.set_mode([WIDTH, HEIGHT])
def print_text (message, x, y, font_color=(0, 0, 0), font_type='etna.otf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button_menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=50):
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

class Button_game:
    def __init__(self, width, height, type):
        self.width = width
        self.height = height
        self.type = type
        self.inactive_color = (205, 41, 144)
        self.active_color = (255, 52, 179)

    def draw(self, x, y, message1, message2, action=None, font_size=50):
        global cost, letal, zaraz, imun, mutation, score
        type = self.type
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and cost<=score:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

                if click[0] == 1:
                    if type == 1:
                        letal = True  # нужно настроить
                    if type == 2:
                        zaraz = True  # тоже
                    if type == 3:
                        imun = True  # тоже
                    if type == 4:
                        mutation = True
                    score -= cost
                    cost += 100
                    button_sound = pygame.mixer.Sound('button2.wav')
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)
                    if action is not None:
                        action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message1, x=x + 10, y=y + 10, font_size=font_size)
        print_text(message2, x=x + (self.width / 2), y=y + 50, font_size=font_size)


def show_menu():
    menu_bg = pygame.image.load('virus.png')
    show = True
    start_b = Button_menu(300, 70)
    quit_b = Button_menu(300, 70)

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
