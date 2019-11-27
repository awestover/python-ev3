# the robot class


"""

STICKS to the wall
"""

import matplotlib.pyplot as plt
import numpy as np
import pygame
import pdb


"""
algorithm

every step update position by current velocity

if you hit a -1 or a 2 change velocity in this manner:

at blacks automatically reverse direction

only backtrack when you hit a deadend surrounded by blacks

"""

square_code = {
	"initial": 0,
	"black visited":-1,
	"white first":1,
	"white second": 2
}

class Robot:
	def __init__(self, imloc, grid_size, pixel_size, mB=None, mC=None):
		self.pos = np.array((0, 0));
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
		new = self.environment[self.pos[0]][self.pos[1]] 
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


	def choose_velocity(self, envcur):
		c_state = self.update_environment(envcur)
		
		if c_state == -1:
			self.vel = -1*self.vel
			return self.vel



		# if c_state == 1:
		# 	if self.vel[0] == 0: # up or down
		# 		if self.pos[0] != self.environment.shape[1]-1 and self.environment[self.pos[1]][self.pos[0]+1] == 0:
		# 			self.vel = np.array((1, 0))
		# 			return self.vel
		# 		elif self.pos[0] != 0 and self.environment[self.pos[1]][self.pos[0]-1] == 0:
		# 			self.vel = np.array((-1, 0))
		# 			return self.vel

		# 	elif self.vel[1] == 0:  # left or right
		# 		if self.pos[1] != self.environment.shape[0]-1 and self.environment[self.pos[1]+1][self.pos[0]] == 0:
		# 			self.vel = np.array((0, 1))
		# 			return self.vel
		# 		elif self.pos[1] != 0 and self.environment[self.pos[1]-1][self.pos[0]] == 0:
		# 			self.vel = np.array((0, -1))
		# 			return self.vel

		# 	return self.vel # do nothing
		# elif c_state == -1:
		# 	self.vel = -1*self.vel
		# 	return self.vel
		# elif c_state == 2:

		# 	if self.vel[0] == 0: # up or down
		# 		if self.pos[0] != self.environment.shape[1]-1 and self.environment[self.pos[1]][self.pos[0]+1] == 0:
		# 			self.vel = np.array((1, 0))
		# 			return self.vel
		# 		elif self.pos[0] != 0 and self.environment[self.pos[1]][self.pos[0]-1] == 0:
		# 			self.vel = np.array((-1, 0))
		# 			return self.vel

		# 	elif self.vel[1] == 0:  # left or right
		# 		if self.pos[1] != self.environment.shape[0]-1 and self.environment[self.pos[1]+1][self.pos[0]] == 0:
		# 			self.vel = np.array((0, 1))
		# 			return self.vel
		# 		elif self.pos[1] != 0 and self.environment[self.pos[1]-1][self.pos[0]] == 0:
		# 			self.vel = np.array((0, -1))
		# 			return self.vel

		# 	return self.vel

	def isAt(self, x, y):
		return self.x == x and self.y == y

	def move_dir(self, xgoal, ygoal):
		next_ = np.array((0, 0))
		if self.x < xgoal:
			next_ = np.array((1, 0))
		elif self.x > xgoal:
			next_ = np.array((-1, 0))
		elif self.y < ygoal:
			next_ = np.array((0, 1))
		elif self.y > ygoal:
			next_ = np.array((0, -1))
		self.facing = self.vel

	def stop_all():
		self.mB.stop(stop_action='brake')
		self.mC.stop(stop_action='brake')

	def run(self, vel):

		# fix it later... backwards is allowed
		while self.facing != self.vel:
			# turn
			# (just b for now for now...)
			self.stop_all()
			mB.run_timed(time_sp=300, speed_sp=500)

			np.dot(np.array([[0, -1], [1, 0]]), self.vel)

		mB.run_timed(time_sp=300, speed_sp=500)
		mC.run_timed(time_sp=300, speed_sp=500)






