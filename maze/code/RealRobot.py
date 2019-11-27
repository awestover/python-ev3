# the robot class

import sys
import os

try:
	import matplotlib.pyplot as plt
	import numpy as np
except ImportError:

	"""
	probably need to do something like
	sudo apt-get install python3-pip

	pip3 install matplotlib

	git pull origin master
	"""

	print("figure it out later...")
	sys.exit()

"""
algorithm
stick to the right

STEP 
TURN (right is black front is white)

matricies y by x
coordinates x then y

environment: 
0: black (or double white)
1: white
-1: not known
"""

rot90 = np.array([[0,-1], [1, 0]])

class Robot:
	def __init__(self, grid_size, motors=[], color_sensors=[]):
		self.pos = np.array((1, 1));
		self.vel = np.array((0, 0));
		self.environment = -1*np.ones(grid_size)
		self.motors = motors
		self.orientation = 0  # radians from original
		self.color_sensors = color_sensors

	def update_pos(self, legit_move=False):  
		self.pos += self.vel
		self.move_vel()
		if legit_move:
			self.environment[self.pos[1]][self.pos[0]] = 0

	def check_adjacent_black(self, vel):
		if self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]] == -1:
			self.vel = vel
			self.update_pos()
			envcur = self.get_state()
			self.environment[self.pos[1]][self.pos[0]] = envcur
			self.vel = -vel
			self.update_pos()
		return self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]]
			

	def choose_velocity(self, vels, c_vals):
		for i in range(0, 4):
			c_forward_idx = i
			# positive rot90 is rotation by 90 since y axis is flipped...
			c_right = np.dot(rot90, vels[i])
			c_right_idx = 0

			for j in range(0, 4):
				if c_right[0] == vels[j][0] and c_right[1] == vels[j][1]:
					c_right_idx = j
					break

			if c_vals[c_right_idx] == 0 and c_vals[c_forward_idx]==1:
				self.vel = vels[i] # INCREDIBLY IMPORTANT
				return vels[i]

		for i in range(0, 4):
			if c_vals[i]==1:
				self.vel = vels[i]
				return vels[i]

		self.display_board(perm=True)
		assert False # throw an error...


	# IFFY
	def get_state(self):
		if self.color_sensors[0].value() < 30:
			return 0
		else:
			return 1

	def isDone(self, bin_maze_px):
		# # print(self.pos, bin_maze_px.shape, "checking")
		# if self.pos[0] == bin_maze_px.shape[1]-1 or self.pos[1] == bin_maze_px.shape[0]-1:
		# 	print("DONE")
		# 	return True
		# if self.pos[0] + self.pos[1] != 0 and self.pos[0] == 0 or self.pos[1] == 0:
		# 	print("DONE")
		# 	return True

		return False

	def display_board(self, perm=False):
		if np.random.random() > 0.9 or perm:
			c_board = self.environment.copy()
			c_board[self.pos[1]][self.pos[0]] = 3
			plt.imshow(c_board)
			plt.pause(0.01)
			if perm:
				plt.savefig(os.path.join("pictures", "robot_brain.png"))
				plt.show()

	def stop_all():
		for motor in self.motors:
			motor.stop(stop_action='brake')
			
	def turn90(self, way):  # way is +- 1
		stop_all()
		self.motors[0].run_timed(time_sp=1000, speed_sp=way*500)

	def straight(self, way):  # way is +- 1
		for motor in self.motors:
			motor.run_timed(time_sp=1000, speed_sp=way*500)

	def move_vel(self):
		# correct heading

		while np.arctan2(this.vel[1], this.vel[0]) - this.orientation > 10**(-2):
			self.turn90(1)
			this.orientation += np.pi/2

		while np.arctan2(this.vel[1], this.vel[0]) - this.orientation < -10**(-2):
			self.turn90(-1)
			this.orientation -= np.pi/2

		# move
		if self.vel[0] + self.vel[1] > 0:
			self.straight(1)
		elif self.vel[0] + self.vel[1] < 0:
			self.straight(-1)

