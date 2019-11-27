# turns an image into a pixel array and outputs it to a csv
import pygame 
import numpy as np
import pandas as pd
import os
import pdb

def getPixelArray(filename):
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image)

maze_name = os.path.join("pictures","maze2.png")

px = getPixelArray(maze_name)

bin_px = np.zeros((px.shape[0], px.shape[1]))

for i in range(0, px.shape[0]):
	for j in range(0, px.shape[1]):
		val = np.sum(px[i][j])/(3*255)

		if val > 0.7:
			bin_px[i][j] = 1
		else:
			bin_px[i][j] = 0


print(bin_px.shape)
df = pd.DataFrame(data=bin_px)
df.to_csv(maze_name.replace(".png", ".csv"), index=False)


