"""
Alek Westover

use the csv we made

NOTE: ONLY DO SHORT PATHS AND YOU MOST LIKELY WILL NOT BREAK IT

CAN you switch theta bands????
"""


"""
mb.run_to_rel_pos(position_sp=-3400) rotates by pi/2 radians (approximentally)
mb.run_timed(time_sp=11500, speed_sp=300) rotates by pi/2 radians (approximentally)

please note:
these times are in millisecconds
but time.sleep takes in seconds!!!

there is a weird thing where we jump theta ranges...
"""

"""
libraries
"""
from Vector import V
from math import pi, isnan, copysign
from random import random
import csv
from time import sleep
from pdb import set_trace as tr

inf = float('inf')

try:
	# TEMPORARY debug tools
	from pprint import pprint
	import pdb
	import matplotlib.pyplot as plt
	import draw_space


	plot_pr = 1

except ImportError:
	from ev3dev.ev3 import *
	# Attach large motors to ports B and C
	mb = LargeMotor('outB')
	mc = LargeMotor('outC')
	
	plot_pr=0

	print("ON Robot")
	def seekTh(goal, cur):
		# get to the theta you need to get to!!!
		# don't continue untill you are there
		# everything else can sleep


		print("start seeking")
		tr()
		dt1 = goal[0] - cur[0]
		dt2 = goal[1] - cur[1]

		# run the one that goes farther at 300
		run_time = int((11500/(pi/2)) * abs(max(dt1, dt2,key=abs)))
		slow_speed = copysign(int(300*min(dt1, dt2,key=abs)/max(dt1, dt2,key=abs)), min(dt1, dt2,key=abs)) 
		fast_speed = copysign(300, max(dt1, dt2,key=abs))

		if dt1<dt2:
			mb.run_timed(time_sp=run_time, speed_sp=fast_speed)
			mc.run_timed(time_sp=run_time, speed_sp=slow_speed)
		else:
			mb.run_timed(time_sp=run_time, speed_sp=slow_speed)
			mc.run_timed(time_sp=run_time, speed_sp=fast_speed)

		sleep(run_time/1000)
		print("done seeking")

	# print("attempt seek")
	# seekTh([1,1], [0,0])
	# tr()


"""
stored theta values
acess thPos with thPos[th1][th2]
"""
thPos = []
th1s = []
th2s = []
ith1s = {}
ith2s = {}


"""
returns a dictionary saying how to get to each index 
of an array from a value
"""
def invertArr(arr):
	di = {}
	for i in range(0, len(arr)):
		di[arr[i]] = i
	return di


"""
parse csv row input
"""
def parse_row(row):
	o = []
	for el in row:
		if el == '':
			pass
		elif el == 'NULL':
			o.append(False)
		elif '_' not in el:
			o.append(float(el))
		else:
			c = el.split('_')
			o.append(V(float(c[0]), float(c[1])))
	return o

"""
parse a single element of data in a csv
"""
def parse_el(el):
	cur = el.split('_')
	return float(cur[0]), float(cur[1])

"""
get data from csv
"""
with open('thPosTable.csv') as csvf:
	read = csv.reader(csvf, delimiter=',')
	first=True
	for row in read:
		if first:
			th1s = parse_row(row)
			first = False
		else:
			th2s.append(float(row[0]))
			thPos.append(parse_row(row[1:]))

"""
make sure that you can look up the values

kinda like a hashtable...

do something like this
thPos[ith2s[th2]][ith1s[th1]]

"""
ith1s = invertArr(th1s)
ith2s = invertArr(th2s)

"""
returns the number which is closest to a given number in a list
"""
def get_closest(arr, num):
	idx = 0
	for i in range(0, len(arr)):
		if abs(arr[i] - num) < abs(arr[idx] - num):
			idx = i
	return arr[idx]

"""
gets the x, y position based on the indices provided
once you deceide on a way of making the grid of sampled thetas, this can be done faster
"""
def getPos(th1, th2):
	try:
		return thPos[ith1s[th1]][ith2s[th2]]
	except KeyError:
		return thPos[ith1s[get_closest(th1s, th1)]][ith2s[get_closest(th2s, th2)]]

"""
distance from pen (given theta values) to a point
Assumes that the referecend location is achievable
"""
def dist(th1, th2, x):
	# these variables can be accessed everywhere but not modified from here
	cc = getPos(th1, th2)
	# print(cc)
	if cc == False:
		return inf
	else:
		return (cc - x).mag()

"""
what should change in th1, th2 be?
does numerical gradient on distance(th1, th2, x)

a little bit problematic in returning nans...
"""
def pt_seek_grad(th1, th2, x):
	epsilon=0.03
	th1u = dist(th1 + epsilon, th2, x)
	th1d = dist(th1 - epsilon, th2, x)
	th2u = dist(th1, th2 + epsilon, x)
	th2d = dist(th1, th2 - epsilon, x)

	j1 = (th1u-th1d)/(2*epsilon)
	j2 = (th2u-th2d)/(2*epsilon)

	update = V(j1, j2)
	update.toUnit()
	rate = 1
	update = update*epsilon*rate

	if isnan(th1-update.x) or isnan(th2-update.y):
		tr()

	return th1-update.x, th2-update.y


"""
what does the gradient look like
"""
def cost_function(goal):
	dists = []
	for th1 in th1s:
		dists.append([])
		for th2 in th2s:
			cPos = getPos(th1, th2)
			if type(cPos) == V:
				dists[-1].append((goal - cPos).mag())
			else:
				dists[-1].append(20)
	return dists

"""
stupid pt search

look at EVERY POSSIBLE theta pair :(((
"""
def pt_seek_stupid(th1, th2, x):
	minDist = inf
	achieved = [th1, th2]

	for t1 in th1s:
		for t2 in th2s:
			cDist = dist(t1, t2, x)
			if cDist < minDist:
				minDist = cDist
				achieved = [t1, t2]

	return achieved

"""
no calculus, simply find the local optimum move
of 4 possible options
"""
def pt_seek(th1, th2, x):
	epsilon = 0.1*(random()+0.5)
	# ths = []
	minDist = inf

	# no change if every move is invalid...
	minTh = [th1, th2]

	# temp debug tool
	# dists = [[0,0],[0,0]]
	
	# idx = 0

	for i in range(0, 3):
		for j in range(0, 3):
			if (i+j != 0):
				cur = [th1, th2]
				cur[0] += (j-1) * epsilon
				cur[1] += (i-1) * epsilon
				# ths.append(cur)
				cDist = dist(cur[0], cur[1], x)
				# dists[i][j]=cDist
				if cDist < minDist:
					# idx = 3*i + j
					minTh = cur
					minDist = cDist

	return minTh #ths[idx], dists


try:
	space_coords = draw_space.sparse_get_pts()
	th_coords = draw_space.getThSpace()
except:
	pass

# th1 = 5.5851
# th2 = 1.7628
th1=0
th2=3.14159

# goal = getPos(th1,th2) + V(random(), random())

# goals = [(-3.5652551952004181, 8.2309451800645537), (-3.498478393183202, 8.5168627849645464), (-3.4150073906616818, 8.8409027371845372), (-3.2425006521172075, 9.1687549241365289), (-3.058864446569864, 9.5957252141205167), (-2.7806277714981311, 9.9960098609805073), (-2.3910964263977048, 10.2438051185605), (-1.6509868707068955, 10.415355681500495), (-0.71054690896443784, 10.464914733016494), (-0.10399095730806085, 10.464914733016494), (0.85870793844013527, 10.377233334180495), (1.5376054256151637, 10.365796629984496), (1.9883488392313708, 10.365796629984496), (2.5615163898791407, 10.167560423920502), (3.2793670115642115, 9.6185986225125166), (3.5631684201373801, 9.0886979947645301), (3.6466394226588985, 8.6083564185325443), (3.5687331536388136, 8.3110021094365525), (3.4240500826015126, 8.1470760159605558), (2.4279627858447093, 8.3376877525605515), (1.9716546387270668, 8.4444303250565476), (1.3762281540735586, 8.4596792639845475), (-0.026084688287975055, 8.5511728975525454), (-0.94426571602469345, 8.4329936208605485), (-1.7233284062255461, 8.4329936208605485), (-2.3465785583862275, 8.3529366914885514), (-2.7194157029823498, 8.2805042315805526), (-3.0532997130684292, 8.2080717716725538), (-3.2703243196243812, 8.1813861285485547)]
"""
get point list from the other csv
"""
goals = []

with open("goalPicture.csv") as csvf:
	read = csv.reader(csvf, delimiter=',')
	xs = []
	firstTime=True
	for row in read:
		if firstTime:
			firstTime = False
		else:
			goals.append(parse_el(row[1]))
print(goals)

goals = [V(xi[0], xi[1]) for xi in goals]


e = 0.3

prevxs = []
prevys = []

# plot_pr = 0

# contours
# cf = cost_function(goals[0])
# plt.imshow(cf)
# plt.show()

try:
	# plotting stuff
	fig, axs = plt.subplots(nrows=2, ncols=2)
except:
	pass


itts = []; dists = [];
i = 0
for goal in goals:
	print("Goal: ", goal)
	dists = []; itts = [];
	while (getPos(th1, th2) - goal).mag() > e and len(dists) < 20:
		# print(len(dists), len(itts))
		cPos = getPos(th1, th2)

		prevys.append(cPos.y); prevxs.append(cPos.x);


		if random() < plot_pr:
			axs[0][0].clear()
			axs[0][0].set_xlim(-15, 15)
			axs[0][0].set_ylim(-15, 15)
			axs[0][0].plot([0, cPos.x], [0,cPos.y], c='k')

			axs[0][0].scatter(space_coords[0], space_coords[1], c='b')

			for agoal in goals:
				axs[0][0].scatter(agoal.x, agoal.y, c='r')

			axs[0][0].scatter(goal.x, goal.y, c='c')
		
		# thc, ds = pt_seek(th1, th2, goal)
		# th1, th2 = thc
		# th1, th2 = pt_seek_grad(th1, th2, goal)
		# th1, th2 = pt_seek(th1, th2, goal)
		
		oldths = [th1, th2]
		th1, th2 = pt_seek_stupid(th1, th2, goal)

		try:
			seekTh([th1, th2], oldths)
		except:
			pass

		# axs[1].clear()
		# axs[1].imshow(ds)
		
		if random() < plot_pr:
			axs[0][1].clear()
			axs[0][1].plot(prevxs, prevys)

			for agoal in goals:
				axs[0][1].scatter(agoal.x, agoal.y, c='r')

			axs[0][1].scatter(cPos.x, cPos.y, c='c')

		itts.append(i)
		dists.append((cPos - goal).mag())

		if random() < plot_pr:
			axs[1][0].clear()
			axs[1][0].plot(itts, dists)
		

		if random() < plot_pr:
			axs[1][1].clear()
			axs[1][1].scatter(th_coords[0], th_coords[1],c='k')
			axs[1][1].scatter(th1, th2, c='c')
	


		if random() < plot_pr:
			plt.pause(0.1)
		i+= 1

		print(th1, th2)

try:
	plt.show()
except:
	print("your picture is ready")