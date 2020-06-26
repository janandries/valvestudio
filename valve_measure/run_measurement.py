import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from datetime import datetime
from list_valve_test_2 import MEASUREMENT_SCHEDULE
from list_valve_test_2 import VALVE_OPEN_TIME

PWM_OUTPUT_PIN = 12

PIC_WAIT_TIME_S = 2
measurements = MEASUREMENT_SCHEDULE

class Setting:
	def __init__(self, freq, duty_cycle, duration):
		self.frequency = freq
		self.dutycycle = duty_cycle
		self.duration = duration


def save_picture(file_name):
	output_folder = "result/"

	print(f"     Saving image {file_name} to {output_folder}{file_name}")
	
	# take picture

	#save picture


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

def get_now_time():
	now = datetime.now()
	return now.strftime("%H%M%S")

def main():
	FILENAME = "result/output.csv"
	camera = PiCamera()

	with open(FILENAME, 'w') as output_file:
		base_file_name = datetime.now().strftime("%Y%m%d")
		
		print(f"Output file: {FILENAME}")
		try:
			configure_valve()

			print(f"Found {len(measurements)} measurments.")

			for n, meas in enumerate(measurements):
				setting = Setting(meas[0], meas[1], VALVE_OPEN_TIME)
				print()
				print(f"[{n}] Starting measurement with freq: {setting.frequency} duty cycle: {setting.dutycycle} for {setting.duration} seconds.")	
				
				start_date = get_date_string()
				start_time = get_time_string()

				start_picture_name = f"{base_file_name}_{get_now_time()}_{n}_start.png"
			
				print(f"     Saving start image to 'result/{start_picture_name}'")
				time.sleep(PIC_WAIT_TIME_S)
				camera.capture('result/' + start_picture_name)
			
				open_valve(setting)

				stop_picture_name = f"{base_file_name}_{get_now_time()}_{n}_stop.png"
				print(f"     Saving stop image to 'result/{stop_picture_name}'")
				time.sleep(PIC_WAIT_TIME_S)
				camera.capture('result/' + stop_picture_name)

				print(f"     Writing results of freq: {setting.frequency}, duty_cycle: {setting.dutycycle}, duration: {setting.duration}")
				output_file.write(f"{start_date},{start_time},{setting.frequency},{setting.dutycycle},{setting.duration},{start_picture_name},{stop_picture_name}\n")

				print("     Done.")

			print("Shutting down")
			cleanup_valve()
		finally:
			GPIO.cleanup()

def test_camera():
	print("Test save picture")
	camera = PiCamera()
	camera.capture('result/' +"test.png")
	print("Done")

if __name__ == "__main__":
	main()
