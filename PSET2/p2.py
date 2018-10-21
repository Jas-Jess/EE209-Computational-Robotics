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
		return(self.grid[s[1], s[0]])

	def reward_grid_5a():
		''' 
			Different reward grid for 5a
		'''
		self.grid =  [
				 [-100, -100, -100, -100, -100, -100], 
				 [-100,    0,  -10,   3,   -10, -100],
				 [-100,    0,  -10,   0,   -10, -100],
				 [-100,    0,  -10,   0,   -10, -100],
				 [-100,    0,    0,   0,     0, -100],
				 [-100, -100, -100, -100, -100, -100]
				]

		self.grid = np.array(self.grid)
		# Flip horizontally, so coordinate points can be referenced easier
		self.grid = np.flip(self.grid, 0)


