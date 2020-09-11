import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from datetime import datetime
from list_valve_test_1 import MEASUREMENT_SCHEDULE
from list_valve_test_1 import VALVE_OPEN_TIME
import os

PWM_OUTPUT_PIN = 12

PIC_WAIT_TIME_S = 2
measurements = MEASUREMENT_SCHEDULE

USE_WEBCAM = False
camera = PiCamera()

REGISTER_PRESSURE = False

class Setting:
	def __init__(self, freq, duty_cycle, duration):
		self.frequency = freq
		self.dutycycle = duty_cycle
		self.duration = duration


def save_picture(folder, file_name):
	print(f"     Saving image {file_name} to {folder}{file_name}")

	if USE_WEBCAM:		
		# take picture
		os.system(f"fswebcam --save {folder}{file_name}") # uses Fswebcam to take picture
	else:
		camera.capture(folder + file_name)

def configure_valve():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PWM_OUTPUT_PIN, GPIO.OUT)
	print(f"Configured valve on PWM pin {PWM_OUTPUT_PIN}")

def cleanup_valve():
	GPIO.cleanup()

def open_valve(setting):
	print(f"     Running valve for {setting.duration} seconds")
	print(f"     freq: {setting.frequency}   duty_cycle: {setting.dutycycle}")
	p = GPIO.PWM(PWM_OUTPUT_PIN, setting.frequency)
	p.start(setting.dutycycle)
	time.sleep(setting.duration)
	p.stop()
	print("     Valve closed")

def get_time_string():
	now = datetime.now()
	return now.strftime("%H:%M:%S")

def get_date_string():
	now = datetime.now()
	return now.strftime("%d-%m-%Y")

def get_now_date():
	now = datetime.now()
	return now.strftime("%Y%m%d")

def get_now_time():
	now = datetime.now()
	return now.strftime("%H%M%S")

def main():
	FILENAME = f"result/{get_now_date()}_{get_now_time()}_output.csv"
	
	#if not USE_WEBCAM:
	#camera = PiCamera()

	with open(FILENAME, 'w') as output_file:
		base_file_name = get_now_date()
		
		print(f"Output file: {FILENAME}")
		try:
			configure_valve()

			print(f"Found {len(measurements)} measurments.")

			if (REGISTER_PRESSURE == False):
				start_pressure = float(input("Pressure will only be recorded at the beginning of the measurements, and enter here: "))
				end_pressure = start_pressure

			for n, meas in enumerate(measurements):
				if (REGISTER_PRESSURE):
					start_pressure = float(input("Adjust pressure to desired value, and enter here: "))

				setting = Setting(meas[0], meas[1], VALVE_OPEN_TIME)
				print()
				print(f"[{n}] Starting measurement with freq: {setting.frequency} duty cycle: {setting.dutycycle} for {setting.duration} seconds.")	
				
				start_date = get_date_string()
				start_time = get_time_string()

				start_picture_name = f"{base_file_name}_{get_now_time()}_{n}_start.png"
			
				print(f"     Saving start image to 'result/{start_picture_name}'")
				time.sleep(PIC_WAIT_TIME_S)
				save_picture('result/', start_picture_name)
			
				open_valve(setting)

				stop_picture_name = f"{base_file_name}_{get_now_time()}_{n}_stop.png"
				print(f"     Saving stop image to 'result/{stop_picture_name}'")
				time.sleep(PIC_WAIT_TIME_S)

				save_picture('result/', stop_picture_name)

				if (REGISTER_PRESSURE):
					end_pressure = float(input("Enter the pressure after messurement (don't adjust yet): "))

				print(f"     Writing results of freq: {setting.frequency}, duty_cycle: {setting.dutycycle}, duration: {setting.duration}")
				output_file.write(f"{start_date},{start_time},{setting.frequency},{setting.dutycycle},{setting.duration},{start_picture_name},{stop_picture_name},{start_pressure},{end_pressure}\n")

				print("     Done.")
				

			print("Shutting down")
		finally:
			GPIO.cleanup()

def test_camera():
	print("Test save picture")
	camera = PiCamera()
	camera.capture('result/' +"test.png")
	print("Done")

if __name__ == "__main__":
	main()
