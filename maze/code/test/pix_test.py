import numpy as np
import pygame
import pygame.surfarray as surfarray

pygame.init()

surface = pygame.display.set_mode((512, 512))

striped = np.zeros((128, 128, 3))
striped[:] = (255, 0, 0)
striped[:,::3] = (0, 255, 255)

# pxarray = pygame.PixelArray(surface)

# pxarray[1:10,:] = (255, 0, 0)


running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	surfdemo_show(striped, 'striped')