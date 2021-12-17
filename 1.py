import math
import pygame

import random

FPS = 30

cost = 100  # стоймость прокачки aka очки/счет

letal = zaraz = imun = 1  # параметры вируса - все это надо интегрировать в код

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
    def __init__(self, screen: pygame.Surface, x, y,xo,yo,N,Repid,Dpropability,propability,active,Name,showstatus,buttonx,buttony):
        self.screen = screen
        #coordinates of left-top and right-bottom angles of city
        self.x = x
        self.y = y
        self.xo = xo
        self.yo = yo
        #number of people
        self.N = N
        #radius, in which the epidemy distributes
        self.Repid = Repid
        #propability to die every day
        self.Dpropability = Dpropability
        #propability of distribution of epidemy (in the radius)
        self.propability = propability
        #activity of people, their velocity
        self.active = active
        #name of city
        self.name = Name
        #status of visualisation on the right part of screen
        self.showstatus = showstatus
        #massive of people who were born in the city
        self.people = []
        #coordinates of button (on the map)
        self.Buttonx = buttonx
        self.Buttony = buttony
    def draw(self):
        #function of drawing on the right part
        pygame.draw.rect(self.screen,WHITE,(coordxramki,coordyramki,self.xo-self.x,self.yo-self.y))



class man:
    def __init__(self, screen: pygame.Surface, ghoust, x, y, live , city):
        self.screen = screen
        #coordinates of people and their radius
        self.x = x
        self.y = y
        self.r = Rusual
        #destination object (if tourist)
        self.destination=city
        #velocity of particle and its angle
        self.v = random.randint(5,10)*0.3
        self.van = random.uniform(0,2*math.pi)
        #color
        self.color = BLUE
        #live index:
        #1 - ill
        #2 - healthy and haven't been ill. Can become ill if the ill person is near
        #0 - healthy and have been ill. Can-t become ill again
        #-1 - dead
        self.live = live
        #city of birth (object)
        self.city = city
        #ghost parametr
        self.ghoust = ghoust
        #time during flight/ride
        self.waytime = 0
        #aim of journey
        self.aimcity = city

        #timer of illness. For healthy people no timer. For ill - time before becoming healthy
        if self.live == 2:
            self.timer = -2
        if self.live == 1:
            self.timer = 14


    #function of moving
    def move(self):
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

        pygame.draw.circle(self.screen,self.color,(self.x+(coordxramki-self.city.x),self.y+(coordyramki-self.city.y)),self.r)


def start_game():
    finished = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    #creating countries
    Countries=[]
    Countries.append(country(screen,1100,350,1425,700,LIGHTRED,'China'))
    Countries.append(country(screen,900,25,1450,300, ORANGE,'Russia'))
    Countries.append(country(screen,590,50,740,350,BLUE,'Netherlands'))
    Countries.append(country(screen,80,170,450,430,DARKBLUE,'USA'))
    Countries.append(country(screen,150,520,500,730,GREEN,'Brasilia'))
    #creating cities and their buttons on the map
    Countries[0].Cities.append(city(screen, -2000, 0, -2000+widthramki, heightramki, 150, 21, 0.015, 0.17, 0.3,'Oohan',1,785,159))
    Countries[0].Cities.append(city(screen, -1600, 0, -1600+widthramki, heightramki, 150, 21, 0.015, 0.17, 0.2,'Beijin',0,843,134))
    Countries[0].Cities.append(city(screen, -1200, 0, -1200+widthramki, heightramki, 150, 21, 0.015, 0.17, 0.2,'Hong-Kong',0,898,185))

    Countries[1].Cities.append(city(screen, -2000, 400, -2000+widthramki, 400+heightramki, 150, 21, 0.02, 0.17, 0.2,'Moscow',0,621,79))
    Countries[1].Cities.append(city(screen, -1600, 400, -1600+widthramki, 400+heightramki, 150, 21, 0.02, 0.17, 0.2,'Chelyabinsk',0,748,72))
    Countries[1].Cities.append(city(screen, -1200, 400, -1200+widthramki, 400+heightramki, 150, 21, 0.02, 0.17, 0.2,'Vladivstok',0,933,98))

    Countries[2].Cities.append(city(screen, -2000, 800, -2000+widthramki, 800+heightramki, 150, 21, 0.02, 0.17, 0.2,'Rotterdam',0,528,90))
    Countries[2].Cities.append(city(screen, -1600, 800, -1600+widthramki, 800+heightramki, 150, 21, 0.02, 0.17, 0.2,'Amsterdam',0,484,123))

    Countries[3].Cities.append(city(screen, -2000, 1200, -2000+widthramki, 1200+heightramki, 150, 21, 0.02, 0.17, 0.2,'Washington',0,224,132))
    Countries[3].Cities.append(city(screen, -1600, 1200, -1600+widthramki, 1200+heightramki, 150, 21, 0.02, 0.17, 0.2,'New York',0,167,159))
    Countries[3].Cities.append(city(screen, -1200, 1200, -1200+widthramki, 1200+heightramki, 150, 21, 0.02, 0.17, 0.2,'Los Anjeles',0,81,149))

    Countries[4].Cities.append(city(screen, -2000, 1600, -2000+widthramki, 1600+heightramki, 150, 21, 0.02, 0.17, 0.2,'Brasilia',0,344,311))
    Countries[4].Cities.append(city(screen, -1600, 1600, -1600+widthramki, 1600+heightramki, 150, 21, 0.02, 0.17, 0.2,'Rio de Janeiro',0,289,346))

    #timer which will work "all day long"
    t=0

    #appending people in the city's massives
    for k in range (len(Countries)):
        for j in range (len(Countries[k].Cities)):
            for i in range (Countries[k].Cities[j].N):
                if k==0 and j==0 and i==0:
                    live=1
                else:
                    live=2
                Countries[k].Cities[j].people.append(man(screen,0,random.uniform(Countries[k].Cities[j].x,Countries[k].Cities[j].xo),random.uniform(Countries[k].Cities[j].y,Countries[k].Cities[j].yo),live,Countries[k].Cities[j]))

    letal_b = Button_game(170, 80, 1)
    zaraz_b = Button_game(170, 80, 2)    # кнопки улучшения вируса
    imun_b = Button_game(170, 80, 3)              

    #start of cycling
    while not finished:
        t=t+1
        screen.fill(WHITE)
        #drawing nearly all things we need on screen
        map = pygame.image.load('map.png')
        screen.blit(map, (0, 0))
        
        letal_b.draw(300, 650, 'Lethality+1', str(cost), None, 30)
        zaraz_b.draw(750, 650, 'Infection+1', str(cost),  None, 30)   # тоже кнопки
        imun_b.draw(1200, 650, 'Immune+1', str(cost),  None, 30)
        #moving All men and drowing Chosen ones and text for country in the viewport on the right
        for k in range(len(Countries)):
            for j in range (len(Countries[k].Cities)):
                if Countries[k].Cities[j].showstatus==1:
                    f = pygame.font.Font(None, 60)
                    text = f.render(str(Countries[k].Cities[j].name), True, (180, 0, 0))
                    screen.blit(text, (1300-12*len(Countries[k].Cities[j].name), 385))

                    g = pygame.font.Font(None, 40)
                    text = g.render(str(Countries[k].name), True, (180, 0, 0))
                    screen.blit(text, (1300-8*len(Countries[k].name),425))

                for i in range (len(Countries[k].Cities[j].people)):
                    if Countries[k].Cities[j].people[i].ghoust==0 and Countries[k].Cities[j].people[i].live!=-1:
                        Countries[k].Cities[j].people[i].move()
                    if Countries[k].Cities[j].showstatus == 1:
                        Countries[k].Cities[j].people[i].draw()
        #drawing ramka above and metki
        ramka = pygame.image.load('Ramka.png').convert_alpha()
        screen.blit(ramka, (1110, 10))
        mapflag = pygame.image.load('metka.png').convert_alpha()


        #moment of giving ilness from one to another
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                screen.blit(mapflag, (Countries[i].Cities[j].Buttonx,Countries[i].Cities[j].Buttony))
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live == 2:
                        for l in range(len(Countries[i].Cities[j].people)):
                            if Countries[i].Cities[j].people[l].ghoust == 0 and Countries[i].Cities[j].people[l].live == 1 and (Countries[i].Cities[j].people[l].x - Countries[i].Cities[j].people[k].x) ** 2 + (Countries[i].Cities[j].people[l].y - Countries[i].Cities[j].people[k].y) ** 2 <= Countries[i].Cities[j].Repid**2 and t % (int(FPS / TK / frequencyofvirus)) == 0 and random.uniform(0, 1) < Countries[i].Cities[j].propability:
                                Countries[i].Cities[j].people[k].live = 1
                                Countries[i].Cities[j].people[k].timer = 14

        # making smaller timer of illneses on people
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live==1  and t%(int(FPS/TK))==0:
                        Countries[i].Cities[j].people[k].timer=Countries[i].Cities[j].people[k].timer-1


        #death or becoming healthy
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live == 1 and t % (int(FPS) / TK) == 0:
                        if random.uniform(0,1)<Countries[i].Cities[j].Dpropability:
                            Countries[i].Cities[j].people[k].live = -1
                    if Countries[i].Cities[j].people[k].timer==-1 and Countries[i].Cities[j].people[k].live==1 and t%(int(FPS)/TK)==0:
                        if random.uniform(0,1)<Countries[i].Cities[j].Dpropability:
                            Countries[i].Cities[j].people[k].live = -1
                        else:
                            Countries[i].Cities[j].people[k].live = 0



        #methods of colouring things
        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live==1:
                        Countries[i].Cities[j].people[k].color=RED
                    if Countries[i].Cities[j].people[k].live==0:
                        Countries[i].Cities[j].people[k].color = GREEN
                    if Countries[i].Cities[j].people[k].live==-1:
                        Countries[i].Cities[j].people[k].color = BLACK

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
def print_text (message, x, y, font_color=(0, 0, 0), font_type='PingPong.otf', font_size=30):
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
        global cost, letal, zaraz, imun
        type = self.type
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

                if click[0] == 1:
                    if type == 1:
                        letal += 1  # нужно настроить
                    if type == 2:
                        zaraz += 1  # тоже
                    if type == 3:
                        imun += 1  # тоже

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
