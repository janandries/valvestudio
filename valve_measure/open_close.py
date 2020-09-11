import time


PWM_PIN = 12
SLEEP_TIME = 60 #seconds
FREQUENCY = 1

import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BOARD)            # choose BCM or BOARD  
GPIO.setup(PWM_PIN, GPIO.OUT) # set a port/pin as an output

print(f"PWM set to {FREQUENCY} Hz, opening time: {SLEEP_TIME} sec")  
p = GPIO.PWM(PWM_PIN, FREQUENCY)
try:
	success = False
	while not success:
		try:
			dc = int(input("Enter duty cycle: "))
			success = True
		except ValueError:
			print("Invalid quanity. Try again")

	print(f"Opening for {SLEEP_TIME} sec with duty cycle {dc} and freq {FREQUENCY}")

		
	p.start(dc)
	time.sleep(SLEEP_TIME)
	p.stop()
	print("done")
finally:
	print("forcing valve to close")
	p.stop()
	p.start(0)
	time.sleep(1)
	p.stop()
	GPIO.cleanup()

