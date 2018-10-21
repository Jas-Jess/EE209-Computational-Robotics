import numpy as np
import itertools
import random

class gridWorld:
	rotation = list(range(0,12))
	action = [['forward','right'],['forward','left'],['forward','none'],['backward','right'],['backward','left'],['backward','none'],['none','none']]

	def __init__(self, L, W, Pe=0):
		self.L = L
		self.W = W
		self.Pe = Pe

		#create state space
		self.S = self.__create_state_space(L,W)
		# Randomly chooses intial state
		self.s = self.S[random.randint(0,len(self.S))]

	def __create_state_space(self,L,W):
		L_list = list(range(0,L))
		W_list = list(range(0,W))

		S_list = [L_list, W_list, self.rotation]

		S_combination = list(itertools.product(*S_list))
		return(S_combination)

	def __action(self,a):
		if a == ['none','none']:
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
				moves foward or backward
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


	def user_defined_action(movement, rotation):
		''' 
			This function takes action and updates current state. 
			Inputs:
				movement = 'foward', 'backward', 'none' 
				rotation = 'right', 'left', 'none'
		'''
		if movement == 'none':
			rotation = 'none'

		self.__action([movement, rotation])
		return

	def random_action():
		'''
			Robot randomly picks an action
		'''
		self.__action(self.action[random.randint(0,len(self.action))])
		return

	def probability(self,s0,a,Pe,s1):
		'''
			if s1 is out of range -> 0
			if s0 == s1 -> 1-2*Pe
			if s0 != s1 but is in range -> Pe
		'''
		#
		if (a == ['none','none']) and (s0 == s1):
			return 1
		elif (abs(s1[0] - s0[0]) > 1) or (abs(s1[1] - s0[1]) > 1):
			return 0
		else:
			sTemp = s0
			#check which direction it's facing
			if 2 <= s0[2] <= 4:	#right
				if a[0] == ['forward']:
					sTemp[0] = sTemp[0] + 1
				elif a[0] == ['backward']:
					sTemp[0] = sTemp[0] - 1
			elif 5 <= s0[2] <= 7:	#down
				if a[0] == ['forward']:
					sTemp[1] = sTemp[1] - 1
				elif a[0] == ['backward']:
					sTemp[1] = sTemp[1] + 1
			elif 8 <= s0[2] <= 10:	#left
				if a[0] == ['forward']:
					sTemp[0] = sTemp[0] - 1
				elif a[0] == ['backward']:
					sTemp[0] = sTemp[0] + 1
			else:					#up
				if a[0] == ['forward']:
					sTemp[1] = sTemp[1] + 1
				elif a[0] == ['backward']:
					sTemp[1] = sTemp[1] - 1


			#do rotation

			if sTemp == s1:
				return (1-2*Pe)
			else:
				return Pe

	def getNextState(self, Pe, s, a):
		# if no action is taken, staying in current state is 100%
		
		if a[0] == 'none':
			return(s)

		# different chances of which movement first
		first_action = np.random.choice(np.array(['movement','right', 'left']), 1, p = [1.0-2.0*Pe, Pe, Pe])

		if first_action != 'movement': 
			s = [s[0], s[1], self.__rotate(first_action, s[2])]

		
		s = list(self.__move(a[0], s))
		s = [s[0], s[1],self.__rotate(a[1], s[2])]

		return s







