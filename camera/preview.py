from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
print("Streaming camera. Press ENTER to quit")
sleep(30)
camera.stop_preview()
