import pygame
from pygame.locals import *
import numpy as np
import random
from scipy.spatial import distance

population_size=100
slow_factor=0.06
life=600
reach=0
gen=1
frame=0
class DNA:
    def __init__(self,gene=[]):
        self.gene_cell=[]
        if gene!=[]:
            self.gene_cell=gene
        else:
            for i in range(life):
                self.gene_cell.append(np.array([random.randint(-1,1),random.randint(-1,1)],dtype=float))
class target:
    def __init__(self):
        self.x=random.randint(width//2,width-20)
        self.y=random.randint(0,(height//3)-20)
    def plot(self):
        pygame.draw.circle(screen,(0,255,0),(self.x,self.y),10)
class Rockets:
    def __init__(self,dna=[]):
        self.position=np.array([200,380],dtype=float)
        self.velocity=np.array([0,0],dtype=float)
        self.acceleration=np.array([0,0],dtype=float)
        self.gene=DNA(dna).gene_cell
        self.count=0
        self.fitness=0
        self.hover=True
        self.wall=False
        self.boundary=False

    def applyForce(self,force):
        self.acceleration+=force*slow_factor

    def update(self):
        global reach
        self.velocity+=self.acceleration
        self.position[0]=(self.position[0]+self.velocity[0])
        self.position[1]=(self.position[1]+self.velocity[1])
        if distance.euclidean((self.position[0],self.position[1]),(t.x,t.y))<=12:
            self.hover=False
            reach+=1
        if (self.position[0]>=rx and self.position[0]<=rx+rw) and (self.position[1]>=ry and self.position[1]<=ry+rh):
            self.wall=True
        if (self.position[0]>=0 and self.position[0]<=width) and (self.position[1]>=0 and self.position[1]<=height):
            self.boundary=True
        self.acceleration=np.array([0,0],dtype=float)

    def calcFitness(self,target):
        dist=distance.euclidean((self.position[0],self.position[1]),(target.x,target.y))
        self.fitness=1/dist

    def show(self):
        pygame.draw.polygon(screen,(255,0,0),((self.position[0]-4,self.position[1]),
                                              (self.position[0],self.position[1]-4),
                                              (self.position[0]+4,self.position[1])),1)
        #pygame.draw.circle(screen,(255,0,0),(int(self.position[0]),int(self.position[1])),4,2)
def selection(pool):
    a=random.choice(pool)
    #pool.remove(a)
    b=random.choice(pool)
    return a,b
def crossover(p1,p2):
    child=[0 for _ in range(len(p1.gene))]
    ind=len(p1.gene)//2

    for i in range(len(child)):
        if i<ind:
            child[i]=p1.gene[i]
        else:
            child[i]=p2.gene[i]

    return child
def mutation(child):
    return DNA(child)
n=0
pygame.init()
pygame.display.set_caption('GENERATION : {}'.format(gen))
width,height=400,400

screen=pygame.display.set_mode((width,height),0,32)
screen.fill((0,0,0))
rockets=[]
for pop in range(population_size):
        rockets.append(Rockets())
t=target()
matingPool=[]
rx,ry,rw,rh=90,220,180,20
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
            if e.key==K_r:
                t=target()
    screen.fill((0,0,0))
    t.plot()
    n+=1
    pygame.draw.rect(screen,(255,255,255),(rx,ry,rw,rh))
    if n%5==0:
        for rocket in rockets:
            if rocket.hover==True and rocket.wall==False:
                rocket.applyForce(rocket.gene[rocket.count])
                rocket.count=(rocket.count+1)%life
                rocket.update()

            rocket.show()
        frame+=1

        ###new Environment creation###
        if frame%1500==0:
            gen+=1
            pygame.display.set_caption('GENERATION : {}'.format(gen))
            print("ROCKETS REACHED : {}/{}".format(reach,population_size))
            reach=0
            for r in rockets:
                r.calcFitness(t)
                if r.wall==True:
                    r.fitness=-10
                if r.boundary==True:
                    r.fitness*=0.00001
            max_val=0
            ##finding max fitness rocket
            for rocket in rockets:
                rocket.fitness*=10**7
                max_val=max(max_val,rocket.fitness)
            ##normaliaztion

            for rocket in rockets:
                rocket.fitness/=max_val
            ##creating mating pool
            for rocket in rockets:
                size=int(rocket.fitness*1000)
                for i in range(size):
                    matingPool.append(rocket)
            ##selection

            childRockets=[]
            for ro in rockets:
                p1,p2=selection(matingPool)
                child=crossover(p1,p2)
                childRockets.append(child)
            rockets=[]
            matingPool=[]
            for c in range(len(childRockets)):
                dna=childRockets[c]
                if random.random()>0.95:
                    dna=[]
                rockets.append(Rockets(dna))

        pygame.display.update()
