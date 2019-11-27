from ev3dev.ev3 import *

print("running")
Sound.beep().wait()
Sound.speak("asdf").wait()

real_size = (512, 512)
scale_fac = 8
pixel_size = (8, 8)
grid_size = (64, 64)

robot = Robot("robot.png", grid_size, pixel_size, 
	mB = LargeMotor('outB'), mC = LargeMotor('outC'))

running = True
while running:
	inp = input("input (x y)")
	x, y = inp.split(" ")
	x, y = int(x), int(y)
	while not robot.isAt(x, y):
		robot.vel = robot.move_dir(x, y)
		robot.update_pos()

	Sound.speak("I have arrived").wait()
      

stop_all()


