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
		self.V = []

		# END OF INIT FUNCTION


	def plot_trajectory(self, s, policy = None, Pe= None):
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
			s = self.gw.get_next_state(Pe, s, a)

			X.append(s[0])
			Y.append(s[1])

			u, v = delta_coord(h_angle_dict[s[2]])
			U.append(u)
			V.append(v)

			if s[0] == self.rg.goal[0] and s[1] == self.rg.goal[1]:
				reward = True
			if a == ['no action', '']:
				break
			

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

	def preallocate_Tprob(self, Pe):
		'''
			This is a preallocation for the transition matrix for all non-zero probs to reduce computational time
			
			Output: 
				T - dictionary indexed by state. In each entry there is [[action], [list of list for all possible next state with probabily]]

		'''

		self.T = {}
		for i in range(len(self.gw.S)):
			s = self.gw.S[i]
			t = []
			for a in self.gw.A:
				t.append([a, self.gw.non_zero_prob(Pe, s, a)])


			self.T[i] = t

		return

	def solve_optimal_policy(self, discount = 0.99, Pe = 0):
		'''
			Function used to solve for the optimal policy 
			by using value iteration. Also, we will assume
			discount will be less than one
		'''
		self.gw.Pe = Pe
		self.preallocate_Tprob(Pe)

		def evaluation_fcn(s,a, Pe, V):
			'''
				evaluation function for value iteration and policy optimization
			'''
			sum_ = 0
			S = np.array(self.gw.S)

			if not(isinstance(a[0], list)):
				next_s = a[0:3]
				prob = a[3]
				s_index = np.where((S == next_s).all(axis=1))
				sum_ += prob*(self.rg.get_reward(s) +discount*V[s_index[0][0]])
				return sum_


			for a_curr in a:

				next_s = a_curr[0:3]
				prob = a_curr[3]
				s_index = np.where((S == next_s).all(axis=1))
				sum_ += prob*(self.rg.get_reward(s) +discount*V[s_index[0][0]])
			# print(sum_)
			return sum_

		def value_iteration():
			'''
				Value iteration until it converges
			'''
			V1 = [0 for i in range(len(self.gw.S))]
			epsilon = 0.001
			while True: 
				V0 = [i for i in V1]
				delta = 0 

				for i in range(len(self.gw.S)):
					s = self.gw.S[i]
					a_sum = []
					for a in (self.T[i]):
						a_sum.append(evaluation_fcn(s,a[1],Pe, V1))
					
					V1[i] = max(a_sum)

					delta = max(delta, abs(V1[i] - V0[i]))


				if delta < 2* epsilon * discount/(1 - discount):
					return V0

		# def policy_opt(V, discount):
		# 	policy = []

		# 	S = np.array(self.gw.S)

		# 	for i in range(len(self.gw.S)):
		# 		max_sum = 0
		# 		max_arg_a = None

		# 		for a in (self.T[i]):
		# 			sum_ = 0
		# 			if not(isinstance(a[1][0], list)):
		# 				next_s = a[1][0:3]
		# 				p_sa = a[1][3]
		# 				idx = np.where((S==next_s).all(axis=1))[0][0]

		# 				sum_ = p_sa*V[idx]

		# 			else:
		# 				for future_s in a[1]:
		# 					next_s = future_s[0:3]
		# 					p_sa = future_s[3]
		# 					idx = np.where((S==next_s).all(axis=1))[0][0]

		# 					sum_ += p_sa*V[idx]

		# 			if sum_ > max_sum or max_arg_a == None:
		# 				max_arg_a = a[0]
		# 				max_sum = sum_

		# 		policy.append(max_arg_a)

		# 	return policy

		def policy_opt(V):
			'''
				Function to get optimal policy with input V
			'''
			policy = []
			

			for i in range(len(self.gw.S)):
				s = self.gw.S[i]
				a_sum = 0
				max_a_val = None 
				max_a = None
				for a in (self.T[i]):
					a_sum = (evaluation_fcn(s,a[1],Pe, V))
					if max_a_val < a_sum or max_a_val == None: 
						max_a_val = a_sum
						max_a = a[0]
					
				policy.append(max_a)


			return policy


		self.V = value_iteration()
		self.policy = policy_opt(self.V)

		return




