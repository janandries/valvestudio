import time


PWM_PIN = 12

import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BOARD)            # choose BCM or BOARD  
GPIO.setup(PWM_PIN, GPIO.OUT) # set a port/pin as an output   
print("Opening!")
GPIO.output(PWM_PIN, 1)       # set port/pin value to 1/GPIO.HIGH/True  
time.sleep(2)
print("Closing")
GPIO.output(PWM_PIN, 0)       # set port/pin value to 0/GPIO.LOW/False  
print("trying PWM")
p = GPIO.PWM(PWM_PIN,100)
p.start(50)
time.sleep(5)
p.stop()
