# move arm simulation

import numpy as np
import matplotlib.pyplot as plt

r = 3 # radius to edges of attachment chord on gear (not gear radius)
l1 = 2  # radius of chord attach
l2 = 5  # length from chord start to end of first rod
l3 = 4  # length of second rod to intersection
l4 = 4 # length of second rod from intersection to end

alpha = np.arccos(1-l1**2/(4*r**2))  # angle between radii to chord

theta0 = np.pi*2/3
theta = theta0
omega = -0.1

coords1 = np.array([-5, 0])  # offset
coords2 = np.array([5, 0])  # offset

# get ends of first rod
def calc_pts(theta, r, mult=1):  # mult is +- 1 flipper
    v1 = np.array([mult*r*np.cos(theta), r*np.sin(theta)])
    v2 = np.array([mult*r*np.cos(theta+alpha), r*np.sin(theta+alpha)])
    v3 = v1 + ((v1-v2) * l2 / np.linalg.norm(v1-v2))
    return v1,v2,v3

def draw_circle(r,ax, translate=np.array([0,0])):
    angs = np.linspace(0, 2*np.pi, 500)
    ax.scatter(r*np.cos(angs)+translate[0], r*np.sin(angs)+translate[1], c='k')

def draw_pts(v, ax, translate=np.array([0,0])):
    v1=v[0]+translate; v2=v[1]+translate; v3=v[2]+translate;
    ax.scatter(v1[0], v1[1], c='r')
    ax.scatter(v2[0], v2[1], c='r')
    ax.scatter(v3[0], v3[1], c='r')

def draw_chords(v, ax, translate=np.array([0,0])):
    v1=translate+v[0]; v2=translate+v[1]; v3=translate+v[2];
    orig=np.array([0,0])+translate
    ax.plot([orig[0],v1[0]], [orig[1],v1[1]], c='g')
    ax.plot([orig[0],v2[0]], [orig[1],v2[1]], c='g')
    ax.plot([orig[0],v3[0]], [orig[1], v3[1]], c='g')
    ax.plot([v1[0],v2[0]], [v1[1],v2[1]], c='g')
    ax.plot([v1[0],v3[0]],[v1[1],v3[1]],c='g')

# get ends of second rods
def calc_cross(x1, x2):
    d = np.linalg.norm(x2-x1)
    print(d, l3)
    th = np.arccos(d/(2*l3))
    be = np.arctan((x2[1]-x1[1])/(x2[0]-x1[0]))
    v4 = (l3+l4)*np.array([np.cos(th + be), np.sin(th+be)])
    v5 = (l3+l4)*np.array([-np.cos(th-be), np.sin(th-be)])
    return v4, v5

# get ends dads way
def calc_cross2(x1,x2):
    print(x1, x2)
    d = np.linalg.norm(x2-x1)
    h = l3*np.sqrt(1-(d/(2*l3))**2)
    ex = (x2-x1)/2
    n = [-ex[1], ex[0]] / (d/2)
    v3 = (x1+ex+h*n)*(l3+l4)/l3
    ex = -ex
    n = -n
    v4 = (x2+ex+h*n)*(l3+l4)/l3
    print(v3, v4)
    return v3, v4

# draw second chords
def draw_chords2(v1i,v4i, ax, translate=np.array([0,0])):
    v1=v1i+translate; v4=v4i+v1;
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
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)

    theta += omega
    if theta> theta0 + np.pi/8 or theta<theta0-np.pi/8:
        omega*=-1

    v1 = calc_pts(theta, r)
    v2 = calc_pts(theta, r, mult=-1)

    draw_circle(r, ax, translate=coords1)
    draw_circle(r, ax, translate=coords2)
    draw_pts(v1, ax, translate=coords1)
    draw_pts(v2, ax, translate=coords2)
    draw_chords(v1, ax, translate=coords1)
    draw_chords(v2, ax, translate=coords2)

    v4, v5 = calc_cross2(v1[2], v2[2])
    draw_chords2(v1[2],v4,ax,translate=coords1)
    draw_chords2(v2[2],v5,ax,translate=coords2)

    plt.pause(0.001)
    if i != MAXI:
        ax.clear()

plt.show()
