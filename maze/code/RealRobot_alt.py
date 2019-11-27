# does not use any non standard libraries... (hard to get on ev3dev...)
# the robot class

import time
import sys
import os

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

def addVec(a, b):
	o = []
	for i in range(0, len(a)):
		o.append(a[i] + b[i])
	return o

def multVec(a, k):
	o = []
	for el in a:
		o.append(k*el)
	return o

def dot(a, b):
	o = []
	for i in range(0, len(a)):
		o.append(a[i]*b[i])
	return o

def multMat(A, x):
	o = []
	for row in A:
		o.append( dot(row, x) )
	return o

def mult(A, k):
	o = []
	for el in A:
		o.append([])
		for e in el:
			o[-1].append(k*e)
	return o

def fillMat(val, size):
	return [[val for j in range(0, size[1])] for i in range(0, size[0])]


def theta(simpleVector):
	if simpleVector == [0, -1]:
		return 270
	if simpleVector == [0, 1]:
		return 90
	if simpleVector == [-1, 0]:
		return 180
	if simpleVector == [1, 0]:
		return 0
	print(self.vel)
	assert False


rot90 = [[0,-1], [1, 0]]

class Robot:
	def __init__(self, grid_size, motors=[], color_sensors=[], gyro):
		self.pos = [1, 1];
		self.vel = [0, 0];
		self.environment = fillMat(-1, grid_size)
		self.motors = motors
		self.gyro  = gyro
		self.orientation = 0  # degrees from gyro should be at
		self.color_sensors = color_sensors

	def update_pos(self, legit_move=False):  
		if self.vel != [0,0]:
			self.pos = addVec(self.pos, self.vel)
			self.move_vel()
			if legit_move:
				self.environment[self.pos[1]][self.pos[0]] = 0

	def check_adjacent_black(self, vel):
		if self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]] == -1:
			self.vel = vel
			self.update_pos()
			envcur = self.get_state()
			self.environment[self.pos[1]][self.pos[0]] = envcur
			self.vel = multVec(vel, -1)
			self.update_pos()
		return self.environment[self.pos[1]+vel[1]][self.pos[0]+vel[0]]
			

	def choose_velocity(self, vels, c_vals):
		print("vels", vels, "c_vals", c_vals)
		for i in range(0, 4):
			c_forward_idx = i
			# positive rot90 is rotation by 90 since y axis is flipped...
			c_right = multMat(rot90, vels[i])
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

		print("error all blacks")
		self.vel = self.vel
		return self.vel
		# assert False # throw an error...


	# slightly IFFY
	def get_state(self):
		if self.color_sensors[0].value() < 30:
			return 0
		else:
			return 1

	def isDone(self):
		# a real robot is never done
		# print(self.pos, bin_maze_px.shape, "checking")
		# if self.pos[0] == bin_maze_px.shape[1]-1 or self.pos[1] == bin_maze_px.shape[0]-1:
		# 	print("DONE")
		# 	return True
		# if self.pos[0] + self.pos[1] != 0 and self.pos[0] == 0 or self.pos[1] == 0:
		# 	print("DONE")
		# 	return True

		return False

	def stop_all(self):
		for motor in self.motors:
			motor.stop(stop_action='brake')
		time.sleep(0.1)

	def turn90(self, way):  # way is +- 1
		self.stop_all()
		self.orientation += 90*way
		while way*self.gyro.value() < way*self.orientation:
			self.motors[0].run_timed(time_sp=100, speed_sp=way*500)
			time.sleep(0.1)
		self.stop_all()

	def straight(self, way):  # way is +- 1
		for motor in self.motors:
			motor.run_timed(time_sp=1000, speed_sp=way*500)
		time.sleep(1)

	def move_vel(self):
		# correct heading

		while theta(self.vel) > self.orientation:
			self.turn90(1)

		while theta(self.vel) < self.orientation:
			self.turn90(-1)

		# move
		if self.vel[0] + self.vel[1] > 0:
			self.straight(1)
		elif self.vel[0] + self.vel[1] < 0:
			self.straight(-1)

