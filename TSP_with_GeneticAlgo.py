import pygame,sys
import tkinter as tk
from pygame.locals import *
import random,time
from tkinter import messagebox,simpledialog
from scipy.spatial import distance
root=tk.Tk()
root.withdraw()

def plotter(x,y,pos,f=-999999999):
    if f==0:
        color=(255,0,0)
    elif f==len(cities)-1:
        color=(0,255,0)
    else:
        color=(0,0,255)

    pygame.draw.circle(screen,color,(x,y),13)
    label = myfont2.render(pos, 3, (255,255,255))
    position=(x-6,y-14)
    screen.blit(label,(position))

def calc_distance(order):
    total=0
    for i in range(len(order)-1):
        total+=distance.euclidean((cities[order[i]].x,cities[order[i]].y),(cities[order[i+1]].x,cities[order[i+1]].y))
    return total

class nodes:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.r=13
        self.color=(0,0,255)
        self.val=len(cities)
    def plot(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)
        label = myfont2.render(str(len(cities)), 3, (255,255,255))
        position=(self.x-6,self.y-14)
        screen.blit(label,(position))

def euclidean(a,b):
    return distance.euclidean((a.x,a.y),(b.x,b.y))
def next_permutation(order):
    n=len(order)
    i=n-2
    while i>=0 and order[i]>=order[i+1]:
        i-=1
    if i==-1:
        return [-99]
    j=i+1
    while j<n and order[j]>order[i]:
        j+=1
    j-=1
    order[i],order[j]=order[j],order[i]
    left=i+1
    right=n-1
    while left<right:
        order[left],order[right]=order[right],order[left]
        left+=1
        right-=1
    return order

pop_size=15
def create_population():
    global cities,pop_size,fitness_arr
    population=[]
    cities_size=[i for i in range(len(cities))]
    for i in range(pop_size):
        fitness_arr.append(10**6)
        copy=cities_size[:]
        random.shuffle(copy)
        population.append(copy)
    return population

def mutation(order):
    a=random.randint(0,len(order)-1)
    b=random.randint(0,len(order)-1)
    order[a],order[b]=order[b],order[a]
    return order

def create_new_population():
    global fitness_arr,pop_size
    best_fitness=0
    best_index=0
    new_pop=[]
    for f in range(len(fitness_arr)):
        if fitness_arr[f] > best_fitness:
            best_fitness=fitness_arr[f]
            best_index=f
    best_order=population[best_index]
    for _ in range(pop_size):
        new_order=mutation(best_order)
        new_pop.append(new_order)
    return new_pop

pygame.init()
pygame.display.set_caption('ITERATIONS ARE {}'.format(''))
screen=pygame.display.set_mode((1000,600),0,32)
screen.fill((255,255,255))
x,y,iters=0,0,0
myfont2 = pygame.font.SysFont("Comic Sans MS", 16)
myfont = pygame.font.SysFont("Comic Sans MS", 20)
label121 = myfont.render('TRAVELLING SALESMAN VISUALIZATION', 5, (255,5,25))
screen.blit(label121,(250,20))
cities=[]
start_end=False
start,end=False,False
start_work,done=False,False
count=0
best_distance=10**10
best_arr=[]
order=[]
fitness_arr=[]
pygame.display.set_caption('ITERATIONS : {}                BEST DISTANCE : {}                PERMUTATION : {}'.format(iters,best_distance,order))

while True:
        for e in pygame.event.get():
            if e.type==KEYDOWN:
                    if e.key==K_q:
                        pygame.quit()
                        sys.exit()
                    if e.key==K_r:
                        screen.fill((255,255,255))
                        x,y=0,0
                        fitness_arr=[]
                        label121 = myfont.render('TRAVELLING SALESMAN PROBLEM', 5, (255,5,25))
                        screen.blit(label121,(250,20))
                        cities,order=[],[]
                        best_arr=[]
                        population=[]
                        best_distance=10**10
                        count=0
                        iters=0
                        done=False
                        start_end=False
                        start,end=False,False
                        start_work=False
                        pygame.display.set_caption('ITERATIONS : {}                BEST DISTANCE : {}                PERMUTATION : {}'.format(iters,best_distance,order))
            if start_work==False:
                if e.type==MOUSEBUTTONDOWN and start_end==False:
                    x,y=pygame.mouse.get_pos()
                    obj=nodes(x,y)
                    obj.plot()
                    cities.append(obj)
                    order.append(len(cities)-1)

                if e.type==KEYDOWN:
                    if e.key==K_q:
                        pygame.quit()
                        sys.exit()
                    if e.key==K_s:
                        start_end=True
                        start=True
                        messagebox.showinfo('HEY THERE!','Nodes are saved')

        if e.type==KEYDOWN and start_work==False:
            if e.key==K_f:
                population=create_population()
                start_work=True
                messagebox.showinfo('HEY THERE!','RED is the START , GREEN is the END')

        if start_work==True and count%40==0 and done==False:
            ##erasing the lines
            for o in range(len(population)):
                order=population[o]
                if order==[-99]:
                    done=True
                    for i in range(len(cities)-1):
                        pygame.draw.line(screen,(0,0,0),(cities[best_arr[i]].x,cities[best_arr[i]].y),(cities[best_arr[i+1]].x,cities[best_arr[i+1]].y),2)
                        plotter(cities[best_arr[i]].x,cities[best_arr[i]].y,str(cities[best_arr[i]].val))
                    for i in range(len(best_arr)-1):
                            pygame.draw.line(screen,(255,0,255),(cities[best_arr[i]].x,cities[best_arr[i]].y),(cities[best_arr[i+1]].x,cities[best_arr[i+1]].y),8)
                            plotter(cities[best_arr[i]].x,cities[best_arr[i]].y,str(cities[best_arr[i]].val),i)
                    plotter(cities[best_arr[-1]].x,cities[best_arr[-1]].y,str(cities[best_arr[-1]].val),len(best_arr)-1)
                if done==False:
                    d=calc_distance(order)
                    fitness_arr[o]=1/d
                    if d<best_distance:
                        for i in range(len(best_arr)-1):
                            pygame.draw.line(screen,(255,255,255),(cities[best_arr[i]].x,cities[best_arr[i]].y),(cities[best_arr[i+1]].x,cities[best_arr[i+1]].y),8)
                            plotter(cities[best_arr[i]].x,cities[best_arr[i]].y,str(cities[best_arr[i]].val),i)

                        best_distance=d
                        best_arr=order[:]

                        for i in range(len(best_arr)-1):
                            pygame.draw.line(screen,(255,0,255),(cities[best_arr[i]].x,cities[best_arr[i]].y),(cities[best_arr[i+1]].x,cities[best_arr[i+1]].y),8)
                            plotter(cities[best_arr[i]].x,cities[best_arr[i]].y,str(cities[best_arr[i]].val),i)

                    ##redrawing the points
                    for i in range(len(cities)-1):
                        pygame.draw.line(screen,(0,0,0),(cities[order[i]].x,cities[order[i]].y),(cities[order[i+1]].x,cities[order[i+1]].y),2)
                        plotter(cities[order[i]].x,cities[order[i]].y,str(cities[order[i]].val))
                    for i in range(len(best_arr)-1):
                            pygame.draw.line(screen,(255,0,255),(cities[best_arr[i]].x,cities[best_arr[i]].y),(cities[best_arr[i+1]].x,cities[best_arr[i+1]].y),8)
                            plotter(cities[best_arr[i]].x,cities[best_arr[i]].y,str(cities[best_arr[i]].val),i)
                    plotter(cities[best_arr[-1]].x,cities[best_arr[-1]].y,str(cities[best_arr[-1]].val),len(best_arr)-1)
                pygame.display.set_caption('ITERATIONS : {}                BEST DISTANCE : {}                PERMUTATION : {}'.format(iters,best_distance,order))
            population=create_new_population()

        count+=1
        #iters+=1
        pygame.display.update()
