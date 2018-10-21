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
			# End of initial policy function

		self.Pe = 0
		self.policy = get_initial_policy()
		self.T = []
		self.past_policy = []
		self.preallocate_Tprob(self.Pe)
		# END OF INIT FUNCTION

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
			s = self.gw.get_next_state(Pe, s, a)

			X.append(s[0])
			Y.append(s[1])

			u, v = delta_coord(h_angle_dict[s[2]])
			U.append(u)
			V.append(v)

			if s[0] == self.rg.goal[0] and s[1] == self.rg.goal[1] and (s[2] == self.rg.goal[2] or self.rg.goal[2] == None):
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
		# END OF PLOT TRAJECTORY 

	def evaluation_function(self, s,a, V, discount):
		'''
			evaluation function for value iteration and policy optimization
		'''
		sum_ = 0
		S = np.array(self.gw.S)

		if not(isinstance(a[0], list)):
			next_s = a[0:3]
			prob = a[3]
			s_index = np.where((S == next_s).all(axis=1))
			sum_ += prob*(self.rg.get_reward(next_s) +discount*V[s_index[0][0]])
			return sum_


		for a_curr in a:

			next_s = a_curr[0:3]
			prob = a_curr[3]
			s_index = np.where((S == next_s).all(axis=1))
			sum_ += prob*(self.rg.get_reward(next_s) +discount*V[s_index[0][0]])
		# print(sum_)
		return sum_


	def policy_evaluation(self, policy = None, discount = 0.99):
		'''
			Value iteration until it converges
		'''
		if policy == None:
			policy = self.policy

		V1 = [0 for i in range(len(self.gw.S))]
		epsilon = 0.00001
		while True: 
		# for _ in range(self.H):
			V0 = [i for i in V1]
			delta = 0 

			for i in range(len(self.gw.S)):
				s = self.gw.S[i]
				a_policy = policy[i]

				for a in (self.T[i]):
					if a[0] == a_policy:
						V1[i] = self.evaluation_function(s,a[1], V1, discount)
						break

				delta = max(delta, abs(V1[i] - V0[i]))


			if delta < 2* epsilon * discount/(1 - discount):
				return V0

		return V1

	def policy_opt(self, V, discount):
		policy = []

		S = np.array(self.gw.S)

		for i in range(len(self.gw.S)):
			max_sum = 0
			max_arg_a = None

			for a in (self.T[i]):
				sum_ = 0
				if not(isinstance(a[1][0], list)):
					next_s = a[1][0:3]
					p_sa = a[1][3]
					idx = np.where((S==next_s).all(axis=1))[0][0]

					# sum_ = p_sa*V[idx]
					sum_ = p_sa*(self.rg.get_reward(next_s) +discount*V[idx])

				else:
					for future_s in a[1]:
						next_s = future_s[0:3]
						p_sa = future_s[3]
						idx = np.where((S==next_s).all(axis=1))[0][0]

						# sum_ += p_sa*V[idx]
						sum_ += p_sa*(self.rg.get_reward(next_s) +discount*V[idx])

				if sum_ > max_sum or max_arg_a == None:
					max_arg_a = a[0]
					max_sum = sum_

			policy.append(max_arg_a)

		return policy


	def solve_optimal_policy(self, policy = None, Pe = 0, discount = 0.99):
		if policy != None:
			self.policy = policy

		self.Pe = Pe
		self.preallocate_Tprob(self.Pe)

		while True:
			self.past_policy = [p for p in self.policy]

			V = self.policy_evaluation(policy = self.policy, discount = discount)
			self.policy = self.policy_opt(V, discount = discount)

			# print''
			# print ''
			# # print(self.policy)
			# print ''
			# print(self.past_policy)

			# Detect no change then policy is solved
			# print(np.array_equal(np.array(self.past_policy), np.array(self.policy)))
			if np.array_equal(np.array(self.past_policy), np.array(self.policy)):
				return 


















