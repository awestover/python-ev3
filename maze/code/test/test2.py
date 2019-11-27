import matplotlib.pyplot as plt
import pygame

def getPixelArray(filename):
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image)

def saveSurface(pixels, filename):
	surf = pygame.surfarray.make_surface(pixels)
	pygame.image.save(surf, filename)

import pdb
pdb.set_trace()
px = getPixelArray("maze.png")


