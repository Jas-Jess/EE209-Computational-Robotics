import numpy as np
from numpy import unravel_index
from p1 import gridWorld
import p2 as reward

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


	def get_policy_eval(self,p,d,Pe,lamda):
		'''
			Compute the policy evaluation of policy pi.
			Inputs: array of policy pi; discount
			Return: array of v = V^pi(s), indexed by state S

			V^pi(s) is initially zero and continuously updated until it converges.
		'''
		self.policy_eval = np.zeros(len(self.gw.S))
		thresh_matrix = np.array(self.policy_eval)
		thresh = 0.0
		
		while thresh < 1.0:
			thresh_matrix = np.array(self.policy_eval)
			for i in range(len(self.gw.S)):
				self.policy_eval[i] += (self.gw.probability(self.gw.S[i],self.policy[i],0.1,self.gw.getNextState(0.1,self.gw.S[i],self.policy[i]))*(reward.get_reward(gw.S[i]) + lamda*self.olicy_eval[i]))

			thresh = abs(sum(self.policy_eval - thresh_matrix)/len(self.gw.S))

		return self.policy_eval


		








