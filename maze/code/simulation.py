# this program will show a simulation of the robot moving

import matplotlib.pyplot as plt
from Robot import Robot
import pandas as pd
import numpy as np
import pdb
import os

"""
bin_maze_px = [\
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
[0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
bin_maze_px = np.array(bin_maze_px)  # y by x
"""

bin_maze_px = np.array(pd.read_csv(os.path.join("pictures", "maze_clean2.csv")))

plt.imshow(bin_maze_px)
plt.savefig(os.path.join("pictures", "mm.png"))

robot = Robot(bin_maze_px.shape)



robot.pos = np.array((3,3))## just because of the mapp delete later!!!!!!!!!!!!


while True:
  robot.update_pos(legit_move=True)
  if not robot.isDone(bin_maze_px):
    vels = [np.array((0, 1)), np.array((0, -1)), np.array((1, 0)), np.array((-1, 0))]
    c_vals = []
    for vel in vels:
      c_vals.append(robot.check_adjacent_black(vel, bin_maze_px))
    robot.choose_velocity(vels, c_vals)
    robot.display_board()

    # print(robot.pos[0], robot.pos[1], "pos")
    # print(vels)
    # print(c_vals)
  else:
    break


robot.display_board(perm=True)

