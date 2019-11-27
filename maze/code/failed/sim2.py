# this program will show a basic simulation of the robot moving


from Robot import Robot
import pygame
import numpy as np
import sys


"""

dimensions


512 X 512 board

but pixel size is 

64 X 64

so scale factor is 

reduce resolution by a factor of 4

robot is 4 X 4 pixels

32 X 32

"""
real_size = (512, 512)
scale_fac = 8
pixel_size = (8, 8)
grid_size = (64, 64)

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
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("ev3 robot simulation")

robot = Robot("robot.png", grid_size, pixel_size);
robot.resize(pixel_size)

maze_pic = pygame.image.load("maze_clean.png")
maze_pic = pygame.transform.scale(maze_pic, real_size)

maze_px = getPixelArray("maze_clean.png")
bin_maze_px = colorArtToBinary(maze_px)

clock = pygame.time.Clock()
running = True


while running:
  clock.tick(5)
 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          sys.exit()
        if event.key == pygame.K_e:
          sys.exit()

  robot.choose_velocity(bin_maze_px[robot.pos[0]][robot.pos[1]])

  screen.blit(maze_pic, (0,0))
  robot.update_pos()
  robot.display(screen)
  pygame.display.flip()

  robot.plot_environment()
