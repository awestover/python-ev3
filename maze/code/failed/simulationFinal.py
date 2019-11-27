# this program will show a simulation of the robot moving
# edge follower

from RobotFinal import Robot
import pygame
import numpy as np
import sys
import pdb


"""
dimensions
512 X 512 board
but pixel size is 
64 X 64
so scale factor is 8
reduce resolution by a factor of 4
robot is 4 X 4 pixels
32 X 32
"""
real_size = (512, 512)
scale_fac = 8
pixel_size = (8, 8)
grid_size = (32, 32)

def getPixelArray(filename):
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image)

def colorToBinary(color):
  if np.sum(color)/(3*255) < 0.5:
    return 0
  else:
    return 1

def colorArtToBinary(colorArr):
  binOut = np.zeros((colorArr.shape[0], colorArr.shape[1]))
  for i in range (0, colorArr.shape[0]):
    for j in range(0, colorArr.shape[1]):
      binOut[i][j] = colorToBinary(colorArr[i][j])
  return binOut

# setup canvas
pygame.init()
screen = pygame.display.set_mode(real_size)
pygame.display.set_caption("ev3 robot simulation")

robot = Robot("robot2.png", grid_size, pixel_size);
robot.resize(pixel_size)

maze_pic = pygame.image.load("maze_clean2.png")
maze_pic = pygame.transform.scale(maze_pic, real_size)

maze_px = getPixelArray("maze_clean2.png")
bin_maze_px = colorArtToBinary(maze_px)

# black them out
# bin_maze_px[0:2,:] = 0
# bin_maze_px[:,0:2] = 0

running = True

print(bin_maze_px)

for r in range(0, 10):
  print(bin_maze_px[r][0:10])



while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          sys.exit()

  screen.blit(maze_pic, (0,0))

  robot.update_pos()
  robot.display(screen)

  # indices 
  vels = [np.array((0, 1)), np.array((0, -1)), np.array((1, 0)), np.array((-1, 0))]
  c_vals = []
  for vel in vels:
    c_vals.append(robot.check_adjacent_black(vel, bin_maze_px))

  print(robot.pos[0], robot.pos[1], "pos")
  print(vels)
  print(c_vals)
  # pdb.set_trace()

  robot.choose_velocity(vels, c_vals)

  pygame.display.flip()
  robot.plot_environment()


