from pygame.locals import *
import pygame
import random,time
from scipy.spatial import distance
from ann import network

ch=1
class slab:
    def __init__(self,pos,col,len=50,width=25,brain=None,j=ch,y=random.randint(0,440)):
        self.x=pos
        self.y=y
        self.width=width
        self.len=60
        self.color=col
        self.displacement=j
        if brain!=None:
            self.brain=brain
        else:
            self.brain=network([1,4,3])
        self.score=0.01

    def update(self,b=None):
        if b!=None:
            self.y=b.y
        else:
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
        self.dx=ch
        self.dy=ch

    def update(self):
        self.x+=self.dx
        self.y+=self.dy

        ##check vertically
        if self.y>=h:
            self.y=h
            self.dy*=-1
        elif self.y<=0:
            self.y=0
            self.dy*=-1

        ##check horizontally

        if self.x<=0:
            p2.score+=3
            self.x=w//2
            self.y=h//2
            self.dx=ch *-1
            self.dy=ch
        elif self.x>=w:
            p1.score+=3
            self.x=w//2
            self.y=h//2
            self.dx=ch *-1
            self.dy=ch

    def collisionp1(self,p1):
        col=False
        ###check contact with slab
        if self.y+self.radius<=p1.y+p1.len and self.y+self.radius>=p1.y:
            if self.dx>0:
                pass
            else:
                self.dx*=-1
            col=True

        return col

    def collisionp2(self,p2):
        col=False
        ##check for slab contact
        if self.y+self.radius<=p2.y+p2.len and self.y+self.radius>=p2.y:
            if self.dx<0:
                pass
            else:
                self.dx*=-1
            col= True

        return col

    def show(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

pygame.init()
w,h=800,500
screen=pygame.display.set_mode((w,h),0,32)
screen.fill((110, 0, 200))

def create_new_population(savedbirds=None,n=None):
    global player1, player2
    if n==0:
        if savedbirds != None:
            total_score = 0
            for b in savedbirds:
                total_score += b.score

            fittest = None
            for b in savedbirds:
                b.fitness = b.score / total_score
                if fittest == None:
                    fittest = b
                elif b.fitness > fittest.fitness:
                    fittest = b

            for i in range(population):
                if random.random() > 0.2:
                    obj = slab(pos=0+30,col=(255,0,0),width=10,len=50,brain=fittest.brain)
                    obj.brain.mutation(0.3)
                else:
                    obj = slab(pos=0+30,col=(255,0,0),width=10,len=50)
                player1.append(obj)
        else:
            for i in range(population):
                obj = slab(pos=0+30,col=(255,0,0),width=10,len=50)
                player1.append(obj)
    elif n==1:
        if savedbirds != None:
            total_score = 0
            for b in savedbirds:
                total_score += b.score

            fittest = None
            for b in savedbirds:
                b.fitness = b.score / total_score
                if fittest == None:
                    fittest = b
                elif b.fitness > fittest.fitness:
                    fittest = b

            for i in range(population):
                if random.random() > 0.2:
                    obj = slab(pos=w-30,col=(0,255,0),width=10,len=50,brain=fittest.brain)
                    obj.brain.mutation(0.4)
                else:
                    obj = slab(pos=w-30,col=(0,255,0),width=10,len=50)
                player2.append(obj)
        else:
            for i in range(population):
                obj = slab(pos=w-30,col=(0,255,0),width=10,len=50)
                player2.append(obj)

def think(slab):
    inp_val=[slab.y-b.y]
    val=slab.brain.predict(inp_val)
    if val==0:
        if slab.displacement<0:
            pass
        else:
            slab.displacement*=-1
    elif val==1:
        if slab.displacement>0:
            pass
        else:
            slab.displacement*=-1
    else:
        slab.displacement=0
    slab.update()

def thinkcon(p,e):
    if e.type==KEYDOWN:
        p.displacement=1
        print('here0')
        if e.key==K_UP:
            if p.displacement>0:
                p.displacement*=-1

        if e.key==K_DOWN:
            if p.displacement<0:
                p.displacement*=-1

#####player creation####
population=100
player1=[]
player2=[]
for _ in range(population):
    player2.append(slab(pos=w-30,col=(0,255,0),width=10,len=50))
b=None
p1,p2=None,None
start=False
balls=[]
gp1,gp2=0,0
move=0
found=False
p2_sc,p1_sc=0,0
p1gen,p2gen=0,0
MAX=2
savedballsp1,savedballsp2=[],[]
myfont = pygame.font.SysFont("Comic Sans MS", 30)
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
            elif e.key==K_s:
                start=True
            elif e.key==K_c:
                p1_sc,p2_sc=0,0
                p1=slab(pos=0+30,col=(255,0,0),width=10,len=50,j=0,y=h//2)
                start=True
                for _ in range(1):
                    balls.append(ball())
                b=balls[0]
            else:
                thinkcon(p1,e)
        elif e.type==KEYUP:
            p1.displacement=0
    ###screen updation###
    screen.fill((110, 0, 200))
    if start:
        ####players updation####
        p1.update()
        p1.show()
        for p2 in player2:
            think(p2)
            p2.update()
            p2.show()
        ####check everything####
        if b.dx>0:
            found=False
            ###check right players
            if b.x>=player2[0].x:
                for i in range(len(player2)-1,-1,-1):
                    p2=player2[i]
                    if b.collisionp2(p2)==False:
                        savedballsp2.append(player2.pop(i))
                    else:
                        p2.score+=1

        elif b.dx<0:
            if b.x<=p1.x+p1.width:
                if b.collisionp1(p1)==False:
                    p2_sc+=1
                    p1=slab(pos=0+30,col=(255,0,0),width=10,len=50,j=0,y=h//2)
                    b=ball()

        if len(player2)==0:
            gp2+=1
            p1_sc+=1
            create_new_population(savedballsp2,1)
            savedballsp2=[]
            ch=5
            b=ball()
            pygame.display.set_caption('gen p1 : {}                     gen p2 : {}'.format(gp1,gp2))
        ####ball update###
        b.update()
        b.show()
        pygame.display.set_caption('P1 : {}                                                              PONG                                                                 p2 : {}'.format(p1_sc,p2_sc))

        if p1_sc ==MAX or p2_sc==MAX:
            start=False
            screen.fill((255,0,0))
            lab1 = myfont.render("YOU LOST LOL!", 45, (110, 0, 200))
            screen.blit(lab1,(50,10))
            lab2 = myfont.render("Press c to Start", 25, (110, 0, 200))
            screen.blit(lab2,(50,80))
    else:
        if p1_sc ==MAX or p2_sc==MAX:
            start=False
            screen.fill((255,0,0))
            lab1 = myfont.render("YOU LOST LOL!", 45, (110, 0, 200))
            screen.blit(lab1,(50,10))
            lab2 = myfont.render("Press c to Start", 25, (110, 0, 200))
            screen.blit(lab2,(50,80))
        else:
            lab2 = myfont.render("Press c to Start", 25, (255, 0, 0))
            screen.blit(lab2,(10,10))
    move+=1
    pygame.display.update()
