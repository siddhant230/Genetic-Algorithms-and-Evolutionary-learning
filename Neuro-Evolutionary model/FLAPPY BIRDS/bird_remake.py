import pygame
from pygame.locals import *
import sys
import random, cv2
import time, math, imutils
import numpy as np
import pickle
from ann import network

bird_img_path1 = 'birdp.png'
bird_img_path2='C:\\Users\\tusha\Downloads\\penguin.png'
bird_img_path3='C:\\Users\\tusha\Downloads\\bird1.png'

pygame.init()
pygame.display.set_caption('FLAPPY BIRD')
w, h = 1000, 700
screen = pygame.display.set_mode((w, h), 0, 32)

bird_img1 = pygame.image.load(bird_img_path1).convert_alpha()
bird_img2 = pygame.image.load(bird_img_path2).convert_alpha()
bird_img3 = pygame.image.load(bird_img_path3).convert_alpha()

y_bird = 165
x_bird = 70
y = 0
move = 0
color = (0, 255, 0)

class bird_create:
	def __init__(self,brain=None):
		self.x=50
		self.y=h//2
		self.score=0
		self.fitness=0
		self.img=random.choice([bird_img1,bird_img2,bird_img3])
		if brain:
			self.brain=brain
		else:
			self.brain=network([4,4,2])

	def update(self,y):
		bird.y += y
		bird.score+=1
		if bird.y > h-20:
			bird.y = h-20
		if bird.y < 25:
			bird.y = 25

	def think(self):
		jump = decide(bird)
		if jump == True:
			y = bird_move_up()
		else:
			y = bird_move_down()
		return y

	def show(self):
		screen.blit(self.img, (bird.x, bird.y))

	def collision(self):
		global closest,pillar
		closest=pillar[0]
		for p in pillar:
			print(p.x,bird.x,closest.x)
			if (p.x-bird.x < closest.x-bird.x and p.x-bird.x>=0) or closest.x<0:
				closest=p
		closest.color=(0,0,255)
		if self.x>closest.x and self.x<closest.x+closest.width_of_pole:
			if self.y<=closest.top or self.y>=closest.top+closest.space:
				return True
			else:
				return False

##pillar banao
class pipe:
	def __init__(self):

		self.top = random.randint(0, h // 2)
		self.bottom = random.randint(0, h // 2)
		self.x = w-50
		self.width_of_pole = 65
		self.speed = 8
		self.score = 0
		self.space=170

	def show(self):
		rectT = (self.x, 0, self.width_of_pole, self.top)
		rectB = (self.x, self.top + self.space, self.width_of_pole, h)
		pygame.draw.rect(screen, color, rectT)
		pygame.draw.rect(screen, color, rectB)

	def update(self):
		self.x -= self.speed

	def collision(self, bx, by):
		if bx > self.x and bx < self.x + self.width_of_pole:
			if by <= self.top or by >= self.top + 170:
				color = (255, 0, 0)
				rect_newT = (self.x, 0, self.width_of_pole, self.top)
				rect_newB = (self.x, self.top + self.space, self.width_of_pole, h)
				pygame.draw.rect(screen, color, rect_newT)
				pygame.draw.rect(screen, color, rect_newB)
				return 1

def create_new_population(savedbirds=None):
	print('############@@@@@@@@@@@@###############')
	global birds,pillar
	if savedbirds!=None:
		total_score=0
		for b in savedbirds:
			total_score+=b.score

		fittest=None
		for b in savedbirds:
			b.fitness=b.score/total_score
			if fittest==None:
				fittest=b
			elif b.fitness>fittest.fitness:
				fittest=b

		for i in range(population):
			if random.random()>0.2:
				obj=bird_create(fittest.brain)
				obj.brain.mutation(0.1)
			else:
				obj=bird_create()
			birds.append(obj)
	else:
		for i in range(population):
			obj=bird_create()
			birds.append(obj)

def bird_move_up():
	gravity = -9.9
	return gravity

def bird_move_down():
	gravity = 9.7
	return gravity

pillar = []

birds=[]
population=100
for i in range(population):
	obj = bird_create()
	birds.append(obj)

def decide(bird):
	global pillar
	closest=pillar[0]
	for p in pillar:
		if p.x-bird.x < closest.x-bird.x and p.x-bird.x>=0 and p.x>0:
			closest=p
	inp_arr=[bird.y , closest.x , closest.top , closest.top+closest.space]
	opt=bird.brain.predict(inp_arr)
	if opt==1:
		return True
	else:
		return False

x_start = 550
press = 0
up = None
start = False
score = 0
gen=0
best=0
savedbirds=[]
while True:
	for e in pygame.event.get():
		if e.type == KEYDOWN:

			if e.key == K_q:
				r=open('weights_flappy.pkl','rb')
				m=pickle.load(r)
				print(m)
				r.close()
				pygame.quit()
				sys.exit()

			if e.key == K_SPACE:
				press = time.time()
				up = True
				y = bird_move_up()

			if e.key == K_c:
				start = True

		if e.type == KEYUP:
			if e.key == K_SPACE:
				y = bird_move_down()
				up = False
	screen.fill((110, 0, 200))

	if start:
		for _ in range(1):

			####pillars####
			if move % 45 == 0:
				pillar.append(pipe())

			for i in range(len(pillar)-1,-1,-1):
				pillar[i].show()
				if move % 2 == 0:
					pillar[i].update()
					for b in birds:
						response = pillar[i].collision(b.x, b.y)
						if response == 1:
							savedbirds.append(birds.pop(birds.index(b)))
				if pillar[i].x<5:
					pillar.pop(i)
					score+=1
			####birds####
			for bird in birds:
				y=bird.think()
				bird.update(y)
				bird.show()
				##making the pillars

			if len(birds)==0:
				gen+=1
				create_new_population(savedbirds)
				score = 0
				move=0
				pillar = []
				pillar.append(pipe())
				savedbirds=[]
			move += 1
	myfont = pygame.font.SysFont("Comic Sans MS", 30)
	lab2 = myfont.render("Press c to Start", 25, (255, 0, 0))
	if start == False:
		screen.blit(lab2, (250, 300))
	best=max(best,score)
	pygame.display.set_caption('GENERATION : {}             score : {}         best score : {}'.format(gen,score,best))
	if best>100:
		with open('weights_flappy.pkl','wb') as f:
			pickle.dump(birds[0].brain.we,f)
		f.close()
	pygame.display.update()
