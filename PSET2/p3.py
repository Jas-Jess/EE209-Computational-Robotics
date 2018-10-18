import matplotlib.pyplot as plt
from p1 import GridWorld2D
from p2 import RewardGrid
import numpy as np 
import math

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


	def plot_trajectory(self, s, policy = None, Pe= 0):
		'''
			Function to plot trajectory given a state
		'''
		h_angle_dict = { 0: 90, 1:60, 2:30, 3:0, 4:330, 5:300, 6:270, 7:240, 8:210, 9:180, 10:150, 11:120  }
		def delta_coord(angle):
		    '''
		    angle - Angle you want your end point at in degrees.
		    '''
		    length = 0.45
		    
		    # find delta
		    deltax = length * math.cos(math.radians(angle))
		    deltay = length * math.sin(math.radians(angle))
		        
		    return deltax, deltay

		if policy == None:
			policy = self.policy


		S = np.array(self.gw.S)
		reward = False
		X = [s[0]]
		Y = [s[1]]

		u, v = delta_coord(h_angle_dict[s[2]])
		U = [u]
		V = [v]

		while(not(reward)):
			s_index = np.where((S == s).all(axis=1))
			print s_index
			a = policy[s_index[0][0]]
			s = self.gw.get_next_state(Pe, s, a)

			X.append(s[0])
			Y.append(s[1])

			u, v = delta_coord(h_angle_dict[s[2]])
			U.append(u)
			V.append(v)

			if s[0] == self.rg.goal[0] and s[1] == self.rg.goal[1]:
				reward = True
			

		plt.figure(figsize=(8,8))
		ax = plt.gca();

		ax.quiver(X[0], Y[0], U[0], V[0], color=['r'],angles='xy', scale_units='xy', scale = 1 )
		ax.quiver(X[1:], Y[1:], U[1:], V[1:], angles='xy', scale_units='xy', scale = 1)

		# Major ticks
		ax.set_xticks(np.arange(0, 6, 1));
		ax.set_yticks(np.arange(0, 6, 1));

		# Labels for major ticks
		ax.set_xticklabels(np.arange(0, 6, 1));
		ax.set_yticklabels(np.arange(0, 6, 1));

		# Minor ticks
		ax.set_xticks(np.arange(-.5, 6, 1), minor=True);
		ax.set_yticks(np.arange(-.5, 6, 1), minor=True);


		# Gridlines based on minor ticks
		ax.grid(which='minor', linestyle='-', linewidth=2)
















