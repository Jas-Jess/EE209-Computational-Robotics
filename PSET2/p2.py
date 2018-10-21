import numpy as np

# This is a specific reward class described in PSET2 problem 2
# 6x6 reward grid
class RewardGrid():
	def __init__(self):

		self.grid =  [
				 [-100, -100, -100, -100, -100, -100], 
				 [-100,    0,  -10,   1,   -10, -100],
				 [-100,    0,  -10,   0,   -10, -100],
				 [-100,    0,  -10,   0,   -10, -100],
				 [-100,    0,    0,   0,     0, -100],
				 [-100, -100, -100, -100, -100, -100]
				]

		self.grid = np.array(self.grid)
		# Flip horizontally, so coordinate points can be referenced easier
		self.grid = np.flip(self.grid, 0)

		# Goal state to get reward
		self.goal = [3, 4, None]

	def get_reward(self, s):
		if self.goal[2] == None:
			return(self.grid[s[1], s[0]])

		if s[0] == self.goal[0] and s[1] == self.goal[1]:
			if s[2] == self.goal[2]: 
				return(self.grid[s[1], s[0]])
			else:
				return 0

		return(self.grid[s[1], s[0]])


	def set_goal(self, s): 
		'''
			Sets new goal
		'''
		self.goal = s
		return

	def reward_grid_5a(self):
		''' 
			Different reward grid for 5a
		'''
		self.grid =  [
				 [-100, -100, -100, -100, -100, -100], 
				 [-100,    0,  -9,   4,   -9, -100],
				 [-100,    0,  -9,   0,   -9, -100],
				 [-100,    0,  -9,   0,   -9, -100],
				 [-100,    0,    0,   0,     0, -100],
				 [-100, -100, -100, -100, -100, -100]
				]

		self.grid = np.array(self.grid)
		# Flip horizontally, so coordinate points can be referenced easier
		self.grid = np.flip(self.grid, 0)
		return


