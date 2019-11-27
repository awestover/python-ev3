#!/usr/bin/env python3
from ev3dev.ev3 import *

btn = Button() # will use any button to stop script

# Attach large motors to ports B and C
mB = LargeMotor('outB')
mC = LargeMotor('outC')

def stop_all():
	mB.stop(stop_action='brake')
	mC.stop(stop_action='brake')

while not btn.any():    # exit loop when any button pressed
    inp = input("input please")
    ev3.Sound.speak(inp).wait()
    if inp == "b":
	    stop_all()
	    mB.run_timed(time_sp=3000, speed_sp=500)
    else:
        stop_all()
	mC.run_timed(time_sp=3000, speed_sp=500)    
      
stop_all()
