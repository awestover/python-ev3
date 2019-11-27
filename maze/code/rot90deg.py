from ev3dev.ev3 import *
import time

print("running")
gy = GyroSensor(); gy.mode='GYRO-ANG'; units = gy.units;
mb = LargeMotor('outB')
theta = gy.value()

# note theta is not the real angle but rather the theoretical angle...
def r(theta):
	while gy.value() < theta:
		mb.run_timed(time_sp=50, speed_sp=500)
	mb.stop(stop_action='brake')

for i in range(0, 8):
	theta += 90
	r(theta)
	print(theta)
	time.sleep(0.4)


"""
get sublime on ev3
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee 
/etc/apt/sources.list.d/sublime-text.list

sudo apt-get update
sudo apt-get install sublime-text

"""