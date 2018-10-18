from p1 import GridWorld2D
from p2 import RewardGrid
import numpy as np 

'''
	This is the policy Iteration class specifically for the gridworld  
	and reward grid described in PSET2 Problem 1 & 2
'''
class PolicyIteration():
	
	def __init__(self):
		self.gw = GridWorld2D(6,6)
		self.rg = RewardGrid()

		def get_initial_policy():
			'''
				Given a certain state, this function will return an 
				initial policy. The initial policy takes action that
				will get close to the goal, regardless of rewards
			'''
			policy = [] # policy matrix
			goal_x = self.rg.goal[0]
			goal_y = self.rg.goal[1]
			


			for i in range(len(self.gw.S)):
				x = self.gw.S[i][0]
				y = self.gw.S[i][1]
				h = self.gw.S[i][2]

				a = [] # Action list

				# First check if (x, y is in reward spot)
				if x == goal_x and y == goal_y:
					policy.append(['no action', ''])
					continue

				x_dir = goal_x - x
				y_dir = goal_y - y

							
				if h in [2,3,4, 8,9,10]:
					# Move left if direction is negative
					if x_dir < 0:
						if h in [2,3,4]: a.append('backward')
						if h in [8,9,10]: a.append('forward')
					# Move right if direction is postive
					elif x_dir >= 0: 
						if h in [2,3,4]: a.append('forward')
						if h in [8,9,10]: a.append('backward')
					
					# No rotation if we are in line with reward
					if y_dir == 0:
						a.append('no rotation')
					# rotate closer to other headings to move up or down
					else:
						if h in [2,8]:
							a.append('left')
						else:
							a.append('right')
					
				elif h in [5,6,7, 11, 0, 1]:
					# Move down if direction is negative
					if y_dir < 0:
						if h in [5,6,7]: a.append('forward')
						if h in [11, 0, 1]: a.append('backward')
					# Move right if direction is postive
					elif y_dir >= 0: 
						if h in [5,6,7]: a.append('backward')
						if h in [11, 0, 1]: a.append('forward')
					
					# No rotation if we are in line with reward
					if x_dir == 0:
						a.append('no rotation')
					# rotate closer to other headings to move right or left
					else:
						if h in [11,5]:
							a.append('left')
						else:
							a.append('right')

				policy.append(a)

			return policy

		self.policy = get_initial_policy()
		# END OF INIT FUNCTION













