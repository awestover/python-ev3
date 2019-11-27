"""
draw something

need to output to csv later
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


x = np.arange(-10,10)
y = x**2

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlim(-4, 4)
ax.set_ylim(8, 11)
ax.plot(x,y)

coords = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print ('x = {}, y= {}'.format(ix, iy))

    global coords
    coords.append((ix, iy))

    plt.scatter(ix, iy)
    plt.pause(0.1)

    if len(coords) == 30:
        fig.canvas.mpl_disconnect(cid)

    return coords

cid = fig.canvas.mpl_connect('button_press_event', onclick)


plt.show()

print(coords)

