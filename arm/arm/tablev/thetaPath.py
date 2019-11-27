"""
If we have a pregenerated list of theta values to visit it is easy to get to them all
"""

"""
needed libraries
"""
from ev3dev.ev3 import *
import csv

from pdb import set_trace as tr
from math import copysign, pi

from time import sleep

"""
parse a single element of data in a csv
"""
def parse_el(el):
	cur = el.split('_')
	return float(cur[0]), float(cur[1])
	
thetaSequence = []
# thetaSequence = [[0,pi],[-0.1,pi+0.1],[-0.2,pi+0.2]]
# read values
with open("thetaPath.csv") as csvf:
	read = csv.reader(csvf, delimiter=',')
	firstTime=True
	for row in read:
		if firstTime:
			firstTime = False
		else:
			thetaSequence.append(parse_el(row[1]))


# Attach large motors to ports B and C
mb = LargeMotor('outB')
mc = LargeMotor('outC')
print("ON Robot")
def seekTh(goal, cur):
	# get to the theta you need to get to!!!
	# don't continue untill you are there
	# everything else can sleep


	print("start seeking")
	tr()
	dt1 = goal[1] - cur[1]
	dt2 = goal[0] - cur[0]

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



for i in range(0, len(thetaSequence)-1):
	seekTh(thetaSequence[i], thetaSequence[i+1])


print("DONE")




