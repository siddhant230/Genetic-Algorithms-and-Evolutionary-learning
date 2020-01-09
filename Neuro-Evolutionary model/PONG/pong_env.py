from pygame.locals import *
import pygame
import random

class slab:
    def __init__(self,pos,col,len=40,width=25):
        self.x=pos
        self.y=h//2
        self.width=width
        self.len=len
        self.color=col
        self.displacement=25
        self.score=0

    def update(self):
        self.y+=self.displacement
        if self.y+self.len>h:
            self.y=h-self.len
        elif self.y<=0:
            self.y=0

    def show(self):
        pygame.draw.rect(screen,(self.color),(self.x,self.y,self.width,self.len))

class ball:
    def __init__(self):
        self.x=w//2
        self.y=h//2
        self.radius=6
        self.color=(255,255,255)
        self.dx=1
        self.dy=1

    def update(self):
        self.x+=self.dx
        self.y+=self.dy

    def collision(self):
        ##collision by slabs
        collision=False
        if collision==False:
            ##check vertically
            if self.y>h:
                self.y=h
                self.dy*=-1
            elif self.y<0:
                self.y=0
                self.dy*=-1

            ##check horizontally
            if self.x<0:
                player2.score+=1
                self.x=w//2
                self.y=h//2
                self.dx=1
                self.dy=1
            elif self.x>w:
                player1.score+=1
                self.x=w//2
                self.y=h//2
                self.dx=1
                self.dy=1

        if (self.x<=player1.x+player1.width and self.x>=player1.x) and (self.y+self.radius>=player1.y and self.y+self.radius<=player1.y+player1.len):
            self.dx*=-1
            collision=True

        elif (self.x>=player2.x and self.x<=player2.x+player2.width) and (self.y+self.radius>=player2.y and self.y+self.radius<=player2.y+player2.len):
            self.dx*=-1
            collision=True


    def show(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

pygame.init()
w,h=460,460
screen=pygame.display.set_mode((w,h),0,32)
screen.fill((110, 0, 200))
def think(e):
    if e.key==K_w:
        if player1.displacement>0:
            player1.displacement*=-1
        player1.update()
    elif e.key==K_e:
        if player1.displacement<0:
            player1.displacement*=-1
        player1.update()
    elif e.key==K_p:
        if player2.displacement<0:
            player2.displacement*=-1
        player2.update()
    elif e.key==K_o:
        if player2.displacement>0:
            player2.displacement*=-1
        player2.update()
#####player creation####
player1=slab(pos=0+30,col=(255,0,0),width=10,len=40)
player2=slab(pos=w-30,col=(0,255,0),width=10,len=40)
b=None
start=False
myfont = pygame.font.SysFont("Comic Sans MS", 30)
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
            elif e.key==K_s:
                start=True
            elif e.key==K_c:
                start=True
                b=ball()
            else:
                think(e)
    ###screen updation###
    screen.fill((110, 0, 200))

    if start:

        b.collision()
        b.update()
        b.show()
        player1.show()
        player2.show()

    else:
        lab2 = myfont.render("Press c to Start", 25, (255, 0, 0))
        screen.blit(lab2,(10,10))
    pygame.display.set_caption('P1 : {}                                                              PONG                                                                 p2 : {}'.format(player1.score,player2.score))
    pygame.display.update()
