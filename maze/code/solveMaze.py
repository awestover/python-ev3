# this program will show a simulation of the robot moving

import matplotlib.pyplot as plt
from RealRobot import Robot
import numpy as np
from ev3dev.ev3 import *
import os

robot = Robot(np.array(64, 64), [LargeMotor('outB'), LargeMotor('outC')], [ColorSensor()])

while True:
  robot.update_pos(legit_move=True)
  if not robot.isDone(bin_maze_px):
    vels = [np.array((0, 1)), np.array((0, -1)), np.array((1, 0)), np.array((-1, 0))]
    c_vals = []
    for vel in vels:
      c_vals.append(robot.check_adjacent_black(vel))
    robot.choose_velocity(vels, c_vals)
    robot.display_board()

    # print(robot.pos[0], robot.pos[1], "pos")
    # print(vels)
    # print(c_vals)
  else:
    break


robot.display_board(perm=True)

