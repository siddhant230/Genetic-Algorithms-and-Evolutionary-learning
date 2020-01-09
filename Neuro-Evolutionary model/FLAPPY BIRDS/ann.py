import random
import numpy as np
import scipy
class network:
	def __init__(self,inp_list):
		self.we=[]
		self.inp=inp_list
		###weight
		for i in range(len(inp_list)-1):
			w=np.random.normal(0.0,1.0,(inp_list[i+1],inp_list[i]))
			self.we.append(w)
		
		###activation function###
		self.lr=100
		
	def sigmoid(self,z):
		return (1/(1+np.exp(-z)))
	
	#######query part#######
	def predict(self,input):
		fin_list=[]
		ip_val=np.array(input)
		val=np.reshape(ip_val,(self.inp[0],1))
		for i in range(len(self.we)):
			fin_list.append(val)
			z=np.dot(self.we[i],val)
			a=self.sigmoid(z)
			val=a
		fin_list.append(val)
		result=list(fin_list[-1])
		ret=result.index(max(result))
		return ret
		
	def mutation(self,rate):
		for j in range(len(self.we)):
			i=self.we[j]
			point_size=i.shape[0]*i.shape[1]
			num_of_mutation=int(rate*point_size)
			
			for _ in range(num_of_mutation):
				row=random.choice(range(i.shape[0]))
				col=random.choice(range(i.shape[1]))
				if random.random()>0.35:
					self.we[j][row][col]+=1/self.lr
				else:
					self.we[j][row][col]-=1/self.lr
