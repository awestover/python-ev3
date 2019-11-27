# move arm simulation

import pdb
import numpy as np
import matplotlib.pyplot as plt

r = 3 # radius to edges of attachment chord on gear (not gear radius)
l1 = 2  # radius of chord attach
l2 = 5  # length from chord start to end of first rod
l3 = 7  # length of second rod to intersection
l4 = 7 # length of second rod from intersection to end

alpha = np.arccos(1-(l1/(2*r))**2)  # angle between radii to chord

theta0 = np.pi*2/3
theta = theta0
omega = -0.1

coords1 = np.array([-5, 0])  # offset
coords2 = np.array([5, 0])  # offset

# get ends of first rod
def calc_pts(theta, r, mult=1, translate=np.array([0,0])):  # mult is +- 1 flipper
    v1 = np.array([mult*r*np.cos(theta), r*np.sin(theta)])
    v2 = np.array([mult*r*np.cos(theta+alpha), r*np.sin(theta+alpha)])
    v3 = v1 + ((v1-v2) * l2 / np.linalg.norm(v1-v2))
    return v1+translate,v2+translate,v3+translate

# draws a circle radius r, center translate
def draw_circle(r,ax, translate=np.array([0,0])):
    angs = np.linspace(0, 2*np.pi, 500)
    ax.scatter(r*np.cos(angs)+translate[0], r*np.sin(angs)+translate[1], c='k')

# get ends dads way
def calc_cross(x1,x2):
    d = np.linalg.norm(x2-x1)
    h = l3*np.sqrt(1-(d/(2*l3))**2)
    ex = (x2-x1)/2
    n = [-ex[1], ex[0]] / (d/2)
    v3 = x1+(ex+h*n)*(l3+l4)/l3
    ex = -ex
    v4 = x2+(ex+h*n)*(l3+l4)/l3
    return v3, v4

# draw second chords
def draw_chords2(v1i,v4i, ax):
    v1=v1i; v4=v4i+v1;
    v5=v4i*l3/(l3+l4)+v1;

    ax.plot([v1[0], v4[0]], [v1[1],v4[1]],c='r')
    ax.scatter([v1[0],v4[0]], [v1[1],v4[1]],c='r')

    ax.plot([v1[0], v5[0]], [v1[1],v5[1]],c='r')
    ax.scatter([v1[0],v5[0]], [v1[1],v5[1]],c='r')



MAXI = 100

fig = plt.figure()
fig.set_size_inches(7, 7)
ax = fig.add_subplot(111)

for i in range(0, MAXI+1):
    ax.set_xlim(-40,40)
    ax.set_ylim(-40,40)

    draw_circle(r, ax, translate=coords1)
    draw_circle(r, ax, translate=coords2)

    theta += omega
    if theta> theta0 + np.pi/8 or theta<theta0-np.pi/8:
        omega*=-1

    v1 = calc_pts(theta, r, translate=coords1)
    v2 = calc_pts(theta, r, mult=-1, translate=coords2)

    for vi in v1:
        ax.scatter(vi[0], vi[1])
    ax.plot([v1[1][0], v1[2][0]], [v1[1][1], v1[2][1]])
    for vi in v2:
        ax.scatter(vi[0], vi[1])
    ax.plot([v2[1][0], v2[2][0]], [v2[1][1], v2[2][1]])

    v4, v5 = calc_cross(v1[2], v2[2])

    draw_chords2(v1[2],v4, ax)
    draw_chords2(v2[2],v5, ax)

    plt.pause(0.001)
    if i != MAXI:
        ax.clear()

plt.show()
