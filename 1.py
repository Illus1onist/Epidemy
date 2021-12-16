import math
import pygame

import random

FPS = 30

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

TK=2
startproc=0.03

Rusual=4
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
class city:
    def __init__(self, screen: pygame.Surface, x, y,xo,yo,N,Repid,Dpropability,propability,active,Name):
        self.screen=screen
        self.x=x
        self.y=y
        self.xo=xo
        self.yo=yo
        self.N=N
        self.Repid=Repid
        self.Dpropability=Dpropability
        self.propability=propability
        self.active=active
        self.name=Name
        self.people=[]
    def draw(self):
        pygame.draw.rect(self.screen,WHITE,(self.x,self.y,self.xo-self.x,self.yo-self.y))


class man:
    def __init__(self, screen: pygame.Surface,ghoust, x, y,live , R,city):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = Rusual
        self.rep=R
        self.v = random.randint(5,10)*0.3
        self.van = random.uniform(0,2*math.pi)
        self.color = BLUE
        self.live = live
        self.city=city
        self.ghoust=ghoust
        self.waytime=0
        self.aimcity=city
        if self.live==2:
            self.timer=-2
        if self.live==1:
            self.timer=14

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
    '''def tourist(self,city1,city2):
        self.ghoust=1
        self.aimcity=city2
        touristmoving(self,city1,city2)
    def Cametothecity(self,city):
        self.city = city
        self.aimcity= city
        self.ghoust=0
    def touristmoving(self,city1,city2,i):
        self.x=(city2.x-city1.x)*i/20+city1.x
        self.x = (city2.y - city1.y)*i/20+city1.y
        self.waytime=self.waytime+1'''

    def draw(self):

        pygame.draw.circle(self.screen,self.color,(self.x,self.y),self.r)

def start_game():
    finished = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    Countries=[]
    Countries.append(country(screen,1100,350,1425,700,LIGHTRED,'China'))
    Countries.append(country(screen,900,25,1450,300, ORANGE,'Russia'))
    Countries.append(country(screen,590,50,740,350,BLUE,'Netherlands'))
    Countries.append(country(screen,80,170,450,430,DARKBLUE,'USA'))
    Countries.append(country(screen,150,520,500,730,GREEN,'Brasilia'))

    Countries[0].Cities.append(city(screen, 1125, 375, 1225, 475, 80, 7, 0.02, 0.1, 0.2,'Oohan'))
    Countries[0].Cities.append(city(screen, 1275, 400, 1375, 500, 80, 7, 0.02, 0.1, 0.2,'Beijin'))
    Countries[0].Cities.append(city(screen, 1200, 540, 1300, 640, 80, 7, 0.02, 0.1, 0.2,'Hong-Kong'))

    Countries[1].Cities.append(city(screen, 995, 175, 1095, 270, 80, 7, 0.02, 0.1, 0.2,'Moscow'))
    Countries[1].Cities.append(city(screen, 925, 50, 1025, 150, 80, 7, 0.02, 0.1, 0.2,'St. Petersburg'))
    Countries[1].Cities.append(city(screen, 1325, 190, 1425, 290, 80, 7, 0.02, 0.1, 0.2,'Vladivstok'))

    Countries[2].Cities.append(city(screen, 605, 200, 705, 300, 80, 7, 0.02, 0.1, 0.2,'Rotterdam'))
    Countries[2].Cities.append(city(screen, 625, 75, 725, 175, 80, 7, 0.02, 0.1, 0.2,'Amsterdam'))

    Countries[3].Cities.append(city(screen, 335, 195, 435, 295, 80, 7, 0.02, 0.1, 0.2,'Washington'))
    Countries[3].Cities.append(city(screen, 325, 320, 425, 420, 80, 7, 0.02, 0.1, 0.2,'New York'))
    Countries[3].Cities.append(city(screen, 110, 270, 210, 370, 80, 7, 0.02, 0.1, 0.2,'Los Anjeles'))

    Countries[4].Cities.append(city(screen, 385, 525, 485, 625, 80, 7, 0.02, 0.1, 0.2,'Brasilia'))
    Countries[4].Cities.append(city(screen, 270, 620, 370, 720, 80, 7, 0.02, 0.1, 0.2,'Rio de Janeiro'))


    t=0
    for k in range (len(Countries)):
        for j in range (len(Countries[k].Cities)):
            for i in range (Countries[k].Cities[j].N):
                if random.uniform(0,1)<=startproc:
                    live=1
                else:
                    live=2
                Countries[k].Cities[j].people.append(man(screen,0,random.uniform(Countries[k].Cities[j].x,Countries[k].Cities[j].xo),random.uniform(Countries[k].Cities[j].y,Countries[k].Cities[j].yo),live,35,Countries[k].Cities[j]))

    def virus():
        menu_bg = pygame.image.load('virus.png')
        virus = True
        one_b = Button(300, 70)
        two_b = Button(300, 70)
        three_b = Button(300, 70)
        four_b = Button(300, 70)
        five_b = Button(300, 70)
        six_b = Button(300, 70)
        seven_b = Button(300, 70)
        eight_b = Button(300, 70)
        nine_b = Button(300, 70)
        back_b = Button(300, 70)
        while virus:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.blit(menu_bg, (0, 0))
            one_b.draw(30, 300, 'Continue game', None, 50)
            two_b.draw(350, 450, 'Continue game', None, 50)
            three_b.draw(350, 150, 'Continue game', None, 50)
            four_b.draw(700, 100, 'Continue game', None, 50)
            five_b.draw(700, 200, 'Continue game', None, 50)
            six_b.draw(700, 400, 'Continue game', None, 50)
            seven_b.draw(700, 500, 'Continue game', None, 50)
            eight_b.draw(1200, 250, 'Continue game', None, 50)
            nine_b.draw(1200, 650, 'Continue game', None, 50)
            back_b.draw(30, 650, 'Back', start_game, 50)

            pygame.display.update()

    virus_b = Button(150, 70)
    while not finished:
        t=t+1
        screen.fill(WHITE)
        map = pygame.image.load('map.png')
        screen.blit(map, (0, 0))
        virus_b.draw(750, 650, 'Virus', virus, 50)
        for k in range(len(Countries)):
            Countries[k].draw()
            g = pygame.font.Font(None, 36)
            text = g.render(str(Countries[k].name), True, (180, 0, 0))
            screen.blit(text, (Countries[k].x, Countries[k].y - 25))
            for j in range (len(Countries[k].Cities)):
                Countries[k].Cities[j].draw()
                f = pygame.font.Font(None, 26)
                text = f.render(str(Countries[k].Cities[j].name), True, (180, 0, 0))
                screen.blit(text, (Countries[k].Cities[j].x, Countries[k].Cities[j].y-18))
                for i in range (len(Countries[k].Cities[j].people)):
                    if Countries[k].Cities[j].people[i].ghoust==0:
                        Countries[k].Cities[j].people[i].move()
                    '''if underMan[i].ghoust==1:
                        underMan[i].touristmoving(self)'''
                    Countries[k].Cities[j].people[i].draw()

        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live == 2:
                        for l in range(len(Countries[i].Cities[j].people)):
                            if Countries[i].Cities[j].people[l].live == 1 and (Countries[i].Cities[j].people[l].x - Countries[i].Cities[j].people[k].x) ** 2 + (Countries[i].Cities[j].people[l].y - Countries[i].Cities[j].people[k].y) ** 2 <= Countries[i].Cities[j].Repid**2 and t % (int(FPS / TK)) == 0 and random.uniform(0, 1) < Countries[i].Cities[j].propability:
                                Countries[i].Cities[j].people[k].live = 1
                                Countries[i].Cities[j].people[k].timer = 14




        for i in range(len(Countries)):
            for j in range(len(Countries[i].Cities)):
                for k in range(len(Countries[i].Cities[j].people)):
                    if Countries[i].Cities[j].people[k].live==1  and t%(int(FPS/TK))==0:
                        Countries[i].Cities[j].people[k].timer=Countries[i].Cities[j].people[k].timer-1



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


        #if t%(int(FPS/TK))==0:
        #   print(Countries[0].Cities[2].people[7].timer) - строчки для проверок в коде


        '''for i in range(len(underMan)):
            if underMan[i].ghoust==0 and random.uniform(0,1)<0.02:
                tourist(underMan[i],underMan[i].city,City[2])'''

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


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        clock.tick(FPS)

Wh = 1500
Ht = 750

screen = pygame.display.set_mode([Wh, Ht])
def print_text (message, x, y, font_color=(0, 0, 0), font_type='PingPong.otf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
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


def show_menu():
    menu_bg = pygame.image.load('virus.png')
    show = True
    start_b = Button(300, 70)
    quit_b = Button(300, 70)

    def show_menu2():
        menu_bg = pygame.image.load('virus.png')
        show2 = True
        primeri_b = Button(300, 70)
        creator_b = Button(300, 70)
        while show2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.blit(menu_bg, (0, 0))
            primeri_b.draw(400, 200, 'New game', start_game, 50)
            creator_b.draw(300, 300, 'Continue game', None, 50)

            pygame.display.update()

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_bg, (0, 0))
        start_b.draw(300, 200, 'Start game', show_menu2, 50)
        quit_b.draw(400, 300, 'Quit game', quit, 50)

        pygame.display.update()

pygame.init()
show_menu()
pygame.quit()
