from ev3dev.ev3 import *
import time
print("running")
gy = GyroSensor(); gy.mode='GYRO-ANG'; units = gy.units;
mb = LargeMotor('outB')
while True:
  inp = int(input("turn time (ms)?"))
  mb.stop(stop_action='brake')
  time.sleep(0.1)
  mb.run_timed(time_sp=inp, speed_sp=500)
  time.sleep(inp/1000)
  print("theta = ", gy.value())