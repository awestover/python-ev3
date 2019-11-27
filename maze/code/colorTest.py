from ev3dev.ev3 import *; import time
c = ColorSensor(); print("running")
while True:
	time.sleep(0.5)
	print(c.value())