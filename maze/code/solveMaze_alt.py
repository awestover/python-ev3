# this program will show a simulation of the robot moving
from RealRobot_alt import Robot
from ev3dev.ev3 import *
import os

robot = Robot([64, 64], [LargeMotor('outB'), LargeMotor('outC')], [ColorSensor()])

print("running")

while True:
  robot.update_pos(legit_move=True)
  if not robot.isDone():
    vels = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    c_vals = []
    for vel in vels:
      c_vals.append(robot.check_adjacent_black(vel))
    robot.choose_velocity(vels, c_vals)
    # robot.display_board()

    # print(robot.pos[0], robot.pos[1], "pos")
    # print(vels)
    # print(c_vals)
  else:
    break

