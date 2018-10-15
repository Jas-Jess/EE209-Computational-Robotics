import numpy as np 
import itertools
import random

class GridWorld2D():
	# Headings
	H = list(range(0,12))
	# Action space
	A = [['foward', 'right'], ['foward', 'left'], 
	     ['backward', 'right'], ['backward', 'left'], 
	     ['foward', 'no rotation'], ['backward', 'no rotation'],
	     ['no action', '']]

	'''
	 *****************
	 PUBLIC FUNCTIONS
	 *****************
	'''
	def __init__(self, L, W, Pe, initial_state = None):
		self.L = L
		self.W = W
		self.Pe = Pe

		# Creating the state space (x,y, h)
		self.S = self.__create_state_space(L, W)

		# Randomly chooses intial state (x, y, h)
		if initial_state == None:
			self.s = list(self.S[random.randint(0,len(self.S))])
		else:
			self.s = list(initial_state)

	def user_defined_action(self,movement, rotation):
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

	def random_action(self):
		'''
			Robot randomly picks an action
		'''
		self.__action(self.A[random.randint(0,len(self.A))])
		return


	def transition_probability(self, Pe, s, a, s_next):
		p_sa = 1
		# if no action is taken, staying in current state is 100%
		if a[0] == 'no action' and s == s_next:
			return(p_sa) 

		p_sa = 0
		# if movement is greater than two, then probability will be zero
		if abs(s[0] - s_next[0]) > 1 or abs(s[1] - s_next[1]) > 1:
			return(p_sa)
		# if you want the state to not be in the bounds, then probability will be zero
		if s_next[0] < 0 or s_next[0] >= self.L or s_next[1] < 0 or s_next[1] >= self.W or !(s_next[2] in H):
			return(p_sa)
		# if you want the robot to rotate anything greater than 2 rotation (accounting for error), then prob will be zero
		r, l = __count_rotation_amount(s[2],s_next[2])
		if r > 2 and l > 2:
			return(p_sa)





	'''
	 *****************
	 PRIVATE FUNCTIONS
	 *****************
	'''

	def __create_state_space(self,L,W):
		'''
			PRIVATE FCN
				creates the state space depending on L and W
		'''
		L_list = list(range(0,L))
		W_list = list(range(0,W))

		S_list = [L_list, W_list, self.H]

		S_combination = list(list(itertools.product(*S_list)))
		return(S_combination)

	def __action(self,a):
		'''
			PRIVATE FCN
				provides action
		'''
		if a == ['no action', '']:
			return

		# picks if movement is first or rotation
		first_action = np.random.choice(np.array(['movement','right', 'left']), 1, p = [1.0-2.0*self.Pe, self.Pe, self.Pe])

		if first_action != 'movement': 
			self.__rotate(first_action)

		self.__move(a[0])
		self.__rotate(a[1])

		return


	def __rotate(self,a):
		'''
			PRIVATE FUNCTION
				Rotates the heading
		'''

		h = self.s[2]

		if a == 'right':
			h += 1

			if h >= 12:
				h = 0

		elif a == 'left':
			h -= 1

			if h < 0:
				h = 11

		self.s[2] = h
		return

	def __move(self,a):
		'''
			PRIVATE FCN
				moves foward or backward
		'''
		x, y, h = self.s

		if a == 'forward':
			if h in [2,3,4]:
				x += 1
			elif h in [5,6,7]:
				y -= 1
			elif h in [8,9,10]:
				x -= 1
			elif h in [11,0,1]:
				y += 1

		elif a == 'backward':
			if h in [2,3,4]:
				x -= 1
			elif h in [5,6,7]:
				y += 1
			elif h in [8,9,10]:
				x += 1
			elif h in [11,0,1]:
				y -= 1

		# Checking if in bound
		if x >= self.L:
			x = self.L -1
		elif x < 0:
			x = 0
		if y >= self.W:
			y = self.W -1
		elif y < 0:
			y = 0

		self.s = list([x, y, h])
		return

	def __count_rotation_amount(self, h, h_next):
		'''
			Private fcn
				Inputs: h and h_next
				outputs: how much rotation to the right and how much rotation to the left 
		'''
		if h_next > h:
			r = h_next - h
			l = 12 - r

		else:
			l = h - h_next
			r = 12 - r 

		return r, l














