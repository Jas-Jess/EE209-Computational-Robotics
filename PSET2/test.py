import numpy as np
from numpy import unravel_index
from p1 import gridWorld
import p2 as reward
from p3 import policyGrid


'''grid = [
		 [-10, -10, -10, -10, -10, -10], 
		 [-10,   0,  -1,   1,  -1, -10],
		 [-10,   0,  -1,   0,  -1, -10],
		 [-10,   0,  -1,   0,  -1, -10],
		 [-10,   0,   0,   0,   0, -10],
		 [-10, -10, -10, -10, -10, -10]
		]

grid = np.array(grid)
grid = np.flip(grid, 0)

goal = unravel_index(grid.argmax(), grid.shape)

print grid[4,3] '''

def get_action_frm_state(s,g):
	'''
		Move towards goal, then rotate in the direction of goal.
	'''
	if s == g:
		return ['none','none']

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

gw = gridWorld(6,6)
pg = policyGrid()

policy = []
for i in range(len(gw.S)):
	policy.append(get_action_frm_state(gw.S[i],(3,4)))

Pe = 0.1


def get_policy_eval(policy,Pe,discount = None, theta=0.00001):
	''' 3d
		Compute the policy evaluation of policy pi.
		Inputs: array of policy pi; discount
		Return: VALUE array of v = V^pi(s), indexed by state S

		V^pi(s) is initially zero and continuously updated until it converges.
	'''
	if discount == None:
		discount = 1.0

	# if policy == None:
	# 	policy = self.policy

	v = np.zeros(len(gw.S)+1)
	
	while True:
		delta = 0
		for s in range(len(gw.S)):
			val = 0

			for i in range(len(policy)):
				val += (gw.probability(gw.S[i],policy[i],Pe,gw.getNextState(Pe,gw.S[i],policy[i]))*(reward.get_reward(gw.S[i]) + discount*v[i+1]))

			delta = max(delta, np.abs(val - v[s]))
			v[s] = val
			
		# print 'Delta: ', delta	
		if delta < theta:
			break
	
	return np.array(v)

v = get_policy_eval(policy,Pe)
# print len(policy)


#3g
def policy_iteration(v,Pe):
	'''
		Computes policy iteration. Returns optimal policy pi^* with optimal value V^*
	'''
	optimal_policy = pg.get_policy(v[0],Pe)
	
	while True:
		# Evaluate the current policy
		V = get_policy_eval(optimal_policy,Pe)
		policy_stable = True

		for s in range(len(gw.S)):
			a = np.argmax(optimal_policy[s])
			print 'a: ',a

			actions = pg.get_policy(V,Pe)
			max_a = np.argmax(actions)
			print 'max a: ', max_a

			if a != max_a:
				policy_stable = False
			optimal_policy[s] = np.eye(len(pg.gw.policy))[max_a]

		if policy_stable:
			return optimal_policy,V


print policy_iteration(v,Pe)
# print pg.get_policy(v[0],Pe)





