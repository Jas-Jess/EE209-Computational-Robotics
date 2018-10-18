import numpy as np 
import itertools
import random

class GridWorld2D():
	# Headings
	H = list(range(0,12))
	# Action space
	A = [['forward', 'right'], ['forward', 'left'], 
	     ['backward', 'right'], ['backward', 'left'], 
	     ['forward', 'no rotation'], ['backward', 'no rotation'],
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
			self.s = list(self.S[random.randint(0,len(self.S)-1)])
		else:
			self.s = list(initial_state)

	def user_defined_action(self,movement, rotation):
		''' 
			This function takes action and updates current state. 
			Inputs:
			 	movement = 'forward', 'backward', 'no action' 
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
		self.__action(self.A[random.randint(0,len(self.A)-1)])
		return


	def transition_probability(self, Pe, s, a, s_next):
		p_sa = 1
		# if no action is taken, staying in current state is 100%
		if a[0] == 'no action' and s == s_next:
			return(p_sa) 

		# create possible state probability according to your action and state
		# There is 1-2*Pe chance that the robot does the correct move/rotation
		x,y,_ = self.__move(a[0], s)
		h = self.__rotate(a[1], s[2])

		if s_next == list([x, y, h]): return (1.0 - 2.0*Pe)

		# There is Pe chance that the robot moves right first
		h = self.__rotate('right', s[2])
		x,y,_ = self.__move(a[0], list([s[0], s[1], h]))
		h = self.__rotate(a[1], h)

		if s_next == list([x, y, h]): return Pe

		# There is Pe chance that the robot moves left first
		h = self.__rotate('left', s[2])
		x,y,_ = self.__move(a[0], list([s[0], s[1], h]))
		h = self.__rotate(a[1], h)

		if s_next == list([x, y, h]): return Pe

		# Any other state will be zero
		return 0

	def get_next_state(self, Pe, s, a):
		# if no action is taken, staying in current state is 100%
		if a[0] == 'no action':
			return(s)

		# different chances of which movement first
		first_action = np.random.choice(np.array(['movement','right', 'left']), 1, p = [1.0-2.0*Pe, Pe, Pe])

		if first_action != 'movement': 
			s[2] = self.__rotate(first_action, s[2])

		s = list(self.__move(a[0], s))
		s[2] = self.__rotate(a[1], s[2])

		return s


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
			self.s[2] = self.__rotate(first_action)

		self.s = list(self.__move(a[0]))
		self.s[2] = self.__rotate(a[1])


		return


	def __rotate(self,a, h = None):
		'''
			PRIVATE FUNCTION
				Rotates the heading
		'''
		if h == None:
			h = self.s[2]

		if a == 'right':
			h += 1

			if h >= 12:
				h = 0

		elif a == 'left':
			h -= 1

			if h < 0:
				h = 11

		return h

	def __move(self,a, s = None):
		'''
			PRIVATE FCN
				moves forward or backward
		'''
		if s == None:
			x, y, h = self.s
		else:
			x, y, h = s

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

		
		return [x, y, h]














