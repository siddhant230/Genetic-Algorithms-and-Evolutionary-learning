import pygame
from pygame.locals import *
import sys,random
import numpy as np
from scipy.spatial import distance
from ann import network

closest_dist=5

class Food:
    def __init__(self,rep):
        self.x=random.randint(30,w-20)
        self.y=random.randint(30,h-20)
        self.rep=rep
        self.position=np.array([self.x,self.y])
        self.radius=3
        if rep==1:
            self.color=(255,255,0)
        else:
            self.color=(255,0,0)
        self.brain=network([2,2])

    def show(self):
        pygame.draw.circle(screen,self.color,self.position,self.radius)

class particle:
    def __init__(self,brain=None):
        self.x=random.randint(100,300)
        self.y=random.randint(100,300)
        self.position=np.array([self.x,self.y],dtype='float64')
        self.radius=10
        self.score=0
        self.r,self.g,self.b=0,255,0
        self.color=(self.r,self.g,self.b)
        if brain:
            self.brain=brain
        else:
            self.brain=network([3,3,2])
        self.velocity=np.random.uniform(0.1,0.9,(2,))
        self.acceleration=np.array([0,0],dtype='float64')
        self.maxforce=0.09
        self.maxspeed=0.09
        self.factor=5


    def update(self):
        p.score-=0.0005
        self.velocity+=self.acceleration
        self.velocity*=self.maxspeed
        self.position+=self.velocity
        self.acceleration*=0

    def eat(self):
        global foods
        closest=None
        best=10**8
        if len(foods)>0:
            for f in foods:
                dist=distance.euclidean((f.x,f.y),self.position)
                if dist<best:
                    best=dist
                    closest=f

            self.seek(closest)

            if best<closest_dist:
                if closest.rep==1:
                    self.score+=1
                    self.g=min(255,100+self.g)
                    self.r=max(0,self.r-150)
                else:
                    self.score-=20
                    self.g=max(0,self.g-150)
                    self.r=min(255,self.r+100)

                foods.pop(foods.index(closest))

    def seek(self,target):
        global foods
        if target!=None:
            desired=target.position-self.position
            steer=desired-self.velocity
            steer*=self.maxforce
            #if distance.euclidean((target.x,target.y),self.position)<closest_dist:
            opt=self.brain.predict([target.rep,target.x,target.y])
            if opt==0:
                val=-1
            elif opt==1:
                val=1
            steer*=val
            self.applyforce(steer)

    def applyforce(self,force):
        self.acceleration+=force

    def show(self):
        pygame.draw.polygon(screen,(self.r,self.g,self.b),((self.position[0]-self.factor,self.position[1]),
                                              (self.position[0],self.position[1]-self.factor),
                                              (self.position[0]+self.factor,self.position[1])))

def create_new_population(savedbirds=None):
    global particles
    rockets=[]
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
        print(fittest.score)
        for i in range(vehicle_population):
            if random.random() > 0.2:
                obj = particle(brain=fittest.brain)
                #obj.brain.mutation(0.1)
            else:
                obj = particle()
            particles.append(obj)
    else:
        for i in range(vehicle_population):
            obj = particle()
            particles.append(obj)

w,h=500,500
pygame.init()
screen=pygame.display.set_mode((w,h),0,32,pygame.HWSURFACE)
screen.fill((110,0,200))

particles=[]
foods=[]
foods.append(Food(rep=random.choice([1,1])))

def new_food_create():
    for _ in range(food_population):
        foods.append(Food(rep=random.choice([-1,1,1])))

vehicle_population,food_population = 10,40
for _ in range(vehicle_population):
    particles.append(particle())
start=False
move=0
gen=0
saved_particles=[]
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
                sys.exit()
            if e.key==K_c:
                new_food_create()
                start=True

    screen.fill((110,0,200))
    if start:
        for p in particles:
            p.eat()
            p.update()
            if p.g<=0 or p.position[0]<=0 or p.position[1]<=0:
                p.score-=0.01
                saved_particles.append(particles.pop(particles.index(p)))
            else:
                p.show()
        for f in foods:
            f.show()

        if len(particles)==0 or len(foods)==0:
            foods=[]
            gen+=1
            saved_particles.extend(particles)
            particles=[]
            create_new_population(saved_particles)
            new_food_create()
    move+=1
    pygame.display.set_caption('GEN : {}'.format(gen))
    pygame.display.update()
