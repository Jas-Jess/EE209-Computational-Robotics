import matplotlib.pyplot as plt
from p1 import GridWorld2D
from p2 import RewardGrid
import numpy as np 
import math

'''
	This is the value iteration class specifically for the gridworld  
	and reward grid described in PSET2 Problem 1 & 2
'''
class ValueIteration():
	
	def __init__(self):
		self.gw = GridWorld2D(6,6)
		self.rg = RewardGrid()

		self.policy = []
		# END OF INIT FUNCTION


	def plot_trajectory(self, s, policy = None, Pe= 0):
		'''
			Function to plot trajectory given a state
		'''
		h_angle_dict = { 0: 90, 1:60, 2:30, 3:0, 4:330, 5:300, 6:270, 7:240, 8:210, 9:180, 10:150, 11:120  }
		def delta_coord(angle):
		    '''
		    OBJECTIVE: Finds 
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
			a = policy[s_index[0][0]]
			print(a)
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

	def solve_optimal_policy(self, Pe = 0, discount = 0.99):
		'''
			Function used to solve for the optimal policy 
			by using value iteration. Also, we will assume
			discount will be less than one
		'''
		self.gw.Pe = Pe
		def value_iteration():
			V1 = [0 for i in range(len(self.gw.S))]
			epsilon = 0.001
			while True: 
				V0 = [i for i in V1]
				delta = 0 

				for i in range(len(self.gw.S)):
					s = self.gw.S[i]
					max_a = V1[i]
					for a in self.gw.A:
						V1[i] = sum([(self.rg.get_reward(s) + self.gw.transition_probability(Pe, s, a, self.gw.S[j])*(discount*V1[j])) for j in range(len(self.gw.S))])
						if max_a > V1[i]: V1[i] = max_a
						else: max_a = V1[i]

					delta = max(delta, abs(V1[i] - V0[i]))

				if delta < epsilon * (1 - discount)/discount:
					return V0


		def policy_opt(V):
			self.policy = []
			for i in range(len(self.gw.S)):
				s = self.gw.S[i]
				max_a_val = None 
				max_a = None

				for a in self.gw.A:
					V[i] = sum([(self.rg.get_reward(s) + self.gw.transition_probability(Pe, s, a, self.gw.S[j])*(discount*V[j])) for j in range(len(self.gw.S))])
					if max_a_val < V[i] or max_a_val == None: 
						max_a_val = V[i]
						max_a = a
						
				self.policy.append(max_a)


			return


		V = value_iteration()
		policy_opt(V)

		return




