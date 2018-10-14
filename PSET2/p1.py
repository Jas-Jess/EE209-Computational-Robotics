import numpy as np 
import itertools
import random

class GridWorld2D():

	h = list(range(0,12))
	A = [['foward', 'right'], ['foward', 'left'], 
	     ['backward', 'right'], ['backward', 'left'], 
	     ['foward', 'no rotation'], ['backward', 'no rotation'],
	     ['no action', '']]

	def __init__(self, L, W, Pe):
		self.L = L
		self.W = W
		self.Pe = Pe

		# Creating the state space
		self.S = self.__create_state_space(L, W)

		# Randomly chooses intial state
		self.s = self.S[random.randint(0,len(self.S))]



	def __create_state_space(L,W):
		'''
			PRIVATE FCN
				creates the state space depending on L and W
		'''
		L_list = list(range(0,L))
		W_list = list(range(0,W))

		S_list = [L_list, W_list, h]

		S_combination = list(itertools.product(*S_list))
		return(S_combination)

	def __action(a):
		'''
			PRIVATE FCN
				provides action
		'''




	def user_defined_action(movement, rotation):
		''' 
			This function takes action and updates current state. 
			Inputs:
			 	movement = 'foward', 'backward', 'no action' 
			 	rotation = 'right', 'left', 'no rotation'

		'''
		if movement == 'no action':
			rotation = ''

		self.__action([movement, rotation])
		return

	def random_action():
		'''
			Robot randomly picks an action
		'''
		self.__action(self.A[random.randint(0,len(self.A))])
		return






