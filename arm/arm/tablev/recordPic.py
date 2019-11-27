"""
draw something

need to output to csv later
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pdb import set_trace as tr

import draw_space


fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlim(-4, 4)
ax.set_ylim(8, 11)

xs, ys = draw_space.get_pts()
ax.scatter(xs, ys, s=1)

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

def csv_form(xy):
    return str(xy[0]) + "_" + str(xy[1])

cid = fig.canvas.mpl_connect('button_press_event', onclick)


plt.show()

coords = [csv_form(ci) for ci in coords]
print(coords)
df = pd.DataFrame.from_dict({"pos": coords})

df.to_csv("goalPicture.csv")



