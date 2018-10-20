import numpy as np
from numpy import unravel_index
from p1 import gridWorld
import p2 as reward
# from sklearn import preprocessing

class policyGrid():
	def __init__(self):

		def get_action_frm_state(self,s,g):
			'''
				Move towards goal, then rotate in the direction of goal.
			'''
			a = ['forward','']

			
			if s[1] < g[1]:		#need to move up
				if s[2] in [11,0,1]:
					a[0] = 'forward'
				elif s[2] in [7,6,5]:
					a[0] = 'backward'

				elif s[2] in [2,3,4]:
					a[1] = 'left'
				elif s[2] in [8,9,10]:
					a[1] = 'right'
			elif s[1] > g[1]:	#need to move down
				if s[2] in [11,0,1]:
					a[0] = 'backward'
				elif s[2] in [7,6,5]:
					a[0] = 'forward'

				elif s[2] in [2,3,4]:
					a[1] = 'right'
				elif s[2] in [8,9,10]:
					a[1] = 'left'
			else:	#s[1] == goal[1]: -> y is equal/robot in the same row as goal
				if s[0] < g[0]:	#need to move right
					if s[2] in [2,3,4]:
						a[0] = 'forward'
					elif s[2] in [8,9,10]:
						a[0] = 'backward'

					elif s[2] in [11,0,1]:
						a[1] = 'right'
					elif s[2] in [7,6,5]:
						a[1] = 'left'
				elif s[0] > g[0]:	#need to move left
					if s[2] in [2,3,4]:
						a[0] = 'backward'
					elif s[2] in [8,9,10]:
						a[0] = 'forward'

					elif s[2] in [11,0,1]:
						a[1] = 'left'
					elif s[2] in [7,6,5]:
						a[1] = 'right'
				#else:	#s[0] == goal[0]: -> x is equal/robot in the same column as goal

			return a

		#using grid and reward from Problem 2
		self.gw = gridWorld(6,6)
		self.policy = []
		for i in range(len(gw.S)):
			self.policy.append(get_action_frm_state(self.gw.S[i],(3,4)))


	def get_policy_eval(self,policy,Pe,lamda):
		''' 3d
			Compute the policy evaluation of policy pi.
			Inputs: array of policy pi; discount
			Return: VALUE array of v = V^pi(s), indexed by state S

			V^pi(s) is initially zero and continuously updated until it converges.
		'''
		policy_eval = np.zeros(len(self.gw.S))
		thresh_matrix = np.array(policy_eval)
		thresh = 0.0
		
		while thresh < 1.0:
			thresh_matrix = np.array(policy_eval)
			for i in range(len(self.gw.S)):
				policy_eval[i] += (self.gw.probability(self.gw.S[i],policy[i],Pe,self.gw.getNextState(Pe,self.gw.S[i],policy[i]))*(reward.get_reward(gw.S[i]) + lamda*self.policy_eval[i]))

			thresh = abs(sum(policy_eval - thresh_matrix)/len(self.gw.S))
			# thresh = preprocessing.normalize([policy_eval - thresh_matrix])

		return policy_eval



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
			s = self.gw.getNextState(Pe, s, a)

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


	#3f
	def get_policy(self,v,Pe,lamda):
		'''
			Returns matrix of policy, given valve v.
		'''
		policy = np.zeros(len(self.gw.S))
		for i in range(1,len(self.gw.S)):
			policy[i] = self.gw.probability(self.gw.S[i],self.policy[i],Pe,self.gw.getNextState(Pe,self.gw.S[i],self.policy[i])) * get_policy_eval(self.policy[i],Pe,lamda)


# get_policy_eval(p,d,Pe,lamda)
# plot_trajectory(s, policy = None, Pe= 0)


		








