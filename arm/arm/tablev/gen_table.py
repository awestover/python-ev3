"""
robot arm movement simulation
Author: Alek Westover

store a look up table
of what theta locations give which x, y coordinates

Conventions:
all angles are in radians
"""

from math import cos, sin, acos, atan, pi
from random import random
from Vector import V
import math

# plotting only stuff
plotting = False
if plotting:
	import matplotlib.pyplot as plt
	import numpy as np

import pandas as pd
import pdb


"""
measure these hyperparameters
"""
# gear angles
th1 = pi
th2 = 0
# on gear measurements
chord_length = 0.75
l2 = 4.5
r = 1 # radius
alpha = acos(1-chord_length**2 / (2*r*r))
# transformations
t1 = V(-1, 0)
t2 = V(1, 0)
# other lengths
l3 = 2.5
l4 = 2.5
l5 = 3
l6 = 0

hyperparameters = {
	"alpha":alpha,
	"t1":t1,
	"t2":t2,
	"r":r,
	"l2":l2,
	"l3":l3,
	"l4":l4,
	"l5":l5,
	"l6":l6,
}


"""
calculation functions
"""

# get the points of the chord on the circle
def on_circle(th1, th2, alpha, t1, t2, r):
	r1 = V(cos(th1), sin(th1)) * r + t1
	r2 = V(cos(th1+alpha), sin(th1+alpha)) * r + t1
	
	r3 = V(cos(th2), sin(th2)) * r + t2
	r4 = V(cos(th2+alpha), sin(th2+alpha)) * r + t2

	return r1,r2,r3,r4

"""
get the first points
"""
def first_pts(r1,r2,r3,r4,l2):
	d1 = r1 - r2
	d1 = d1 * (l2 / d1.mag()) + r1
	
	d2 = r4 - r3 #  (note this is - what the other one is kind of not really...)
	d2 = d2 * (l2 / d2.mag()) + r4
	
	return d1,d2


"""
extend from previous points to farther out
"""
def after_cross(x1, x2, l3, l4):
	try:
		B = acos((x2 - x1).mag()/(2*l3))
		
		ex = (x2 - x1) * (1 / 2)
		n = ex.getPerp()
		h1 = ex*(1)  + n * l3*sin(B)
		h2 = ex*(-1) + n * l3*sin(B)
		
		v1 = x1 + h1*((l3+l4)/l3)
		v2 = x2 + h2*((l3+l4)/l3)
		return v1,v2

	except:
		# domain ERROR
		# print("arccos domain error")
		return False

"""
functions to help invert the function
"""
def get_thetas(r1, r2):
	vs = []
	for i in range(0, r1):
		v1cur = 2*pi*i/r1
		for j in range(0, r2):
			v2cur = 2*pi*j/r2
			vs.append((v1cur, v2cur))
	return vs

"""
gets ther location of the pen point
"""
def pen_point(th1, th2, hparams):
	alpha=hparams["alpha"];t1=hparams["t1"];t2=hparams["t2"];r=hparams["r"];
	l2=hparams["l2"];
	l3=hparams["l3"];l4=hparams["l4"];
	l5=hparams["l5"];l6=hparams["l6"];

	r1,r2,r3,r4=on_circle(th1, th2, alpha, t1, t2, r)
	d1,d2=first_pts(r1,r2,r3,r4,l2)
	d3,d4=after_cross(d1, d2, l3, l4)
	d5,d6=after_cross(d4,d3,l5,l6)

	return d6

"""
get the distance from the pen point to the desired point
note if x=V(0,0) this is the distance from the origin
"""
def dist(th1, th2, x, hyperparameters):
	d6 = pen_point(th1, th2, hyperparameters)
	return (d6 - x).mag()

"""
what should change in th1, th2 be?
does numerical gradient on distance(th1, th2, x)
"""
def pt_seek_grad(th1, th2, x, hyperparameters):
	epsilon=0.01
	th1u = dist(th1+epsilon, th2, x, hyperparameters)
	th1d = dist(th1, th2, x, hyperparameters)
	th2u = dist(th1, th2+epsilon, x, hyperparameters)
	th2d = dist(th1, th2, x, hyperparameters)

	j1 = (th1u-th1d)/(epsilon)
	j2 = (th2u-th2d)/(epsilon)

	update = V(j1, j2)
	update.toUnit()
	rate = 1
	update = update*epsilon*rate
	print(update)

	return th1-update.x, th2-update.y


"""
creates a list of every way of combining an element from each of 2 lists
list will have size n choose 2
"""
def perm(l1, l2):
	o = []
	for i in l1:
		for j in l2:
			o.append((i, j))
	return o

"""
what should I do to get closer to the point? 
options are all permutations of both motors being off or positive or negative rotation
"""
def pt_seek(th1, th2, x, hyperparameters):
	dist_eps = 0.1
	eps=0.01
	ds = []
	ths = [[th1, th1+eps, th1-eps],[th2, th2+eps, th2-eps]]
	# ths = [[],[]]
	# n = 10
	# ths[0] = [th1+eps*2*i/n-eps for i in range(0, n)]
	# ths[1] = [th2+eps*2*i/n-eps for i in range(0, n)]
	ths_agg = perm(ths[0], ths[1])

	min_idx = None
	for i in range(0, len(ths_agg)):
		ds.append(dist(ths_agg[i][0], ths_agg[i][1], x, hyperparameters))
		if min_idx == None or ds[-1] < ds[min_idx]:
			# if ths_agg[i][0] == th1 and ths_agg[i][1] == th2:
			if i == 0:  # means it is the 0,0 change one
				if ds[-1] < dist_eps:
					print("0,0 chosen",ds[-1])
					min_idx = i
			else:
				min_idx = i

	print("pt_seek, min_idx", min_idx)
	noise = 0
	noised_ths_aggs = [ths_agg[min_idx][0]+random()*noise*eps,ths_agg[min_idx][1]+random()*noise*eps]
	return  noised_ths_aggs

"""
format a x y pair for putting in the csv
"""
def csv_form(x, y):
	return str(round(x, 4)) + "_"+ str(round(y,4))

"""
plotting functions
"""
def plot_chord(r1,r2,r3,r4,ax):
	for r in [r1,r2,r3,r4]:
		ax.scatter(r.x,r.y,c='k')
	ax.plot([r1.x,r2.x],[r1.y,r2.y],c='k')
	ax.plot([r3.x,r4.x],[r3.y,r4.y],c='k')

def plot_arm(start, end, ax):
	ax.plot([start.x, end.x], [start.y,end.y],c='b')
	ax.scatter([start.x, end.x], [start.y,end.y],c='b')

def plot_circle(t, r, ax):
	angs = np.linspace(0, 2*pi)
	ax.plot(r*np.cos(angs)+t.x, r*np.sin(angs)+t.y,c='r')

# def plot_path(path, ax):
# 	ax.scatter([pathi.x for pathi in path], [pathi.y for pathi in path], c='r')
# 	# ax.plot([pathi.x for pathi in path], [pathi.y for pathi in path], c='r')

if plotting:
	# fig2=plt.figure()
	# ax2=fig2.add_subplot(111)

	fig=plt.figure()
	fig.set_size_inches(7, 7)
	ax=fig.add_subplot(111)

"""
testing grid search
"""
s = 360
path = []
dists = []
thetas = get_thetas(int(s),int(s))


"""
store positions
pos_stored = {"th1": {"th2": "value"}}
"""
pos_stored = {}

"""
main loop
"""
print("running")
for i in range(0, len(thetas)): # grid search

	th1=thetas[i][0]
	th2=thetas[i][1]

	sth1 = str(round(th1, 4))
	sth2 = str(round(th2, 4))

	try:
		pos_stored[sth1][sth2] = ""
	except KeyError:
		pos_stored[sth1] = {sth2:""}

	# print(th1,th2)

	if plotting:

		ax.clear()
		ax.set_xlim(-10,20)
		ax.set_ylim(-10,20)

	try:
		r1,r2,r3,r4=on_circle(th1, th2, alpha, t1, t2, r)
		d1,d2=first_pts(r1,r2,r3,r4,l2)
		d3,d4=after_cross(d1, d2, l3, l4)
		d5,d6=after_cross(d4,d3,l5,l6)

		if d3.mag() < d1.mag() or d5.mag() < d3.mag():
			assert False

		if d6.mag() < d4.mag() or d4.mag() < d2.mag():
			assert False

		pos_stored[sth1][sth2] = csv_form(d6.x, d6.y)

		if plotting:

			plot_circle(t1, r, ax)
			plot_circle(t2, r, ax)

			plot_chord(r1,r2,r3,r4,ax)
			plot_arm(r1,d1,ax)
			plot_arm(r3,d2,ax)
			plot_arm(d1,d3,ax)
			plot_arm(d2,d4,ax)
			plot_arm(d3,d5,ax)
			plot_arm(d4,d6,ax)

			plt.pause(0.1)
	
	except:
		pos_stored[sth1][sth2] = "NULL"


print("DONEDONEDONE")
print(pos_stored)
df = pd.DataFrame(pos_stored)
df.to_csv("thPosTable.csv")

if plotting:
	plt.savefig("execution.png")
	plt.show()

