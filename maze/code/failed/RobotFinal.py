# the robot class

import matplotlib.pyplot as plt
import numpy as np
import pygame
import pdb


"""
algorithm
stick to the right

STEP 
TURN (right is black front is white)
"""


"""
matricies y by x

coordinates x then y

"""


rot90 = np.array([[0,-1], [1, 0]])

class Robot:
	def __init__(self, imloc, grid_size, pixel_size, mB=None, mC=None):
		self.pos = np.array((3, 2));
		self.vel = np.array((0, 1));
		self.image = pygame.image.load(imloc);
		self.environment = np.zeros(grid_size)  # big matrix
		self.pixel_size = pixel_size
		self.facing = np.array((1, 0))
		self.mB = mB
		self.mC = mC

	def update_pos(self, dt=1):  # dt should really by 1, not time strictly but a step...
		self.pos += self.vel * dt;
		
	def display(self, screen):
		screen.blit(self.image, (self.pos[0]*self.pixel_size[0], self.pos[1]*self.pixel_size[1]));

	def resize(self, size):
		self.image = pygame.transform.scale(self.image, size);

	def plot_environment(self):
		plt.imshow(self.environment.T);
		plt.savefig("environment.png");

	def update_environment(self, envcur):
		new = self.environment[self.pos[1]][self.pos[0]] 
		if envcur == 0:# black
			new = -1
		else:
			if new == 1:
				new = 2
			else:
				new = 1

		# acess by Y first!!!!
		self.environment[self.pos[1]][self.pos[0]] = new;
		return new


	def check_adjacent_black(self, vel, bin_maze_px):
		# pdb.set_trace()
		# print(self.pos, vel)
		if self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]] == 0:
			self.vel = vel
			self.update_pos()
			envcur = self.get_state(self.pos[0], self.pos[1], bin_maze_px)
			self.update_environment(envcur)
			self.vel = -vel
			self.update_pos()
			return envcur
		else:
			c_val = self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]]
			if c_val == -1:
				return 0 # black
			else:
				return 1  # not unvisited and not black.... 

	def choose_velocity(self, vels, c_vals):
		for i in range(0, 4):
			# pdb.set_trace()

			c_right= np.dot(rot90, vels[i])  # positive rot90 is rotation by 90 since y axis is flipped...
			c_right_idx = 0

			for j in range(0, 4):
				if c_right[0] == vels[j][0] and c_right[1] == vels[j][1]:
					c_right_idx = j
					break

			c_forward_idx = i

			if c_vals[c_right_idx] == 0 and c_vals[c_forward_idx]==1:
				return vels[i]

		for i in range(0, 4):
			if c_vals[i]==1:
				return vels[i]


	def isAt(self, x, y):
		return self.x == x and self.y == y

	def stop_all():
		self.mB.stop(stop_action='brake')
		self.mC.stop(stop_action='brake')

	def run(self, vel):

		# fix it later... backwards is allowed
		while False:
		# while self.facing != self.vel:
			# turn
			# (just b for now for now...)
			self.stop_all()
			mB.run_timed(time_sp=300, speed_sp=500)

			np.dot(-rot90, self.vel)  # real world 90 degrees is like this

		mB.run_timed(time_sp=300, speed_sp=500)
		mC.run_timed(time_sp=300, speed_sp=500)


	def get_state(self, i, j, bin_maze_px):
		return bin_maze_px[j][i]


