import pygame 
import numpy as np

def getPixelArray(filename):
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image)

def saveSurface(pixels, filename):
	surf = pygame.surfarray.make_surface(pixels)
	pygame.image.save(surf, filename)


px = getPixelArray("maze2.png")

# px[:][0] = np.array((0,0,0))
# px[:][0:3] = np.array((0,0,0))
# px[0:10][0:10] = np.array((0,0,0))

# px[0:30][0:30] = np.array((0,0,0))

# import pdb
# pdb.set_trace()


#px[0][0] = np.array((255, 255, 255))
#px[1][0] = np.array((255, 255, 255))
#px[0][1] = np.array((255, 255, 255))

px[0:2,:] = np.array((0,0,0))
px[:,0:2] = np.array((0,0,0))


for i in range(0, px.shape[0]):
	for j in range(0, px.shape[1]):
		val = np.sum(px[i][j])/(3*255)
		print(val)

		if val > 0.7:
			px[i][j] = np.array((255,255,255))
		else:
			px[i][j] = np.array((0,0,0))

saveSurface(px, "maze_clean2.png")


