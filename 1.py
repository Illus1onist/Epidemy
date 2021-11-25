import math
import pygame

import random

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1000
HEIGHT = 700

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

pygame.init()

finished = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
Countries=[]
Countries.append(country(screen,50,50,500,500,RED,'China'))

Countries[0].Cities.append(city(screen, 100, 100, 200, 200, 80, 7, 0.4, 0.1, 0.2,'Oohan'))
Countries[0].Cities.append(city(screen, 300, 100, 400, 200, 80, 7, 0.4, 0.1, 0.2,'Beijin'))
Countries[0].Cities.append(city(screen, 100, 300, 200, 400, 80, 7, 0.4, 0.1, 0.2,'Hong-Kong'))

t=0
for k in range (len(Countries)):
    for j in range (len(Countries[k].Cities)):
        for i in range (Countries[k].Cities[j].N):
            if random.uniform(0,1)<=startproc:
                live=1
            else:
                live=2
            Countries[k].Cities[j].people.append(man(screen,0,random.uniform(Countries[k].Cities[j].x,Countries[k].Cities[j].xo),random.uniform(Countries[k].Cities[j].y,Countries[k].Cities[j].yo),live,35,Countries[k].Cities[j]))




while not finished:


    t=t+1
    screen.fill(WHITE)
    for k in range(len(Countries)):
        Countries[k].draw()
        for j in range (len(Countries[k].Cities)):
            Countries[k].Cities[j].draw()
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


pygame.quit()
