import numpy as np

# This is a specific reward class described in PSET2 problem 2
# 6x6 reward grid
class RewardGrid():
	def __init__(self):

		self.grid =  [
				 [-10, -10, -10, -10, -10, -10], 
				 [-10,   0,  -1,   1,  -1, -10],
				 [-10,   0,  -1,   0,  -1, -10],
				 [-10,   0,  -1,   0,  -1, -10],
				 [-10,   0,   0,   0,   0, -10],
				 [-10, -10, -10, -10, -10, -10]
				]

		self.grid = np.array(self.grid)
		# Flip horizontally, so coordinate points can be referenced easier
		self.grid = np.flip(self.grid, 0)

	def get_reward(self, s):
		return(self.grid[s[1], s[0]])

