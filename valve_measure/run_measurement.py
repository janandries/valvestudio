import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from datetime import datetime

PWM_OUTPUT_PIN = 12

VALVE_OPEN_TIME = 60 # seconds
measurements = [[100, 0.5],	[50,  0.5]]

class Setting:
	def __init__(self, frequency, duty_cycle, duration):
		self.frequency = frequency
		self.dutycycle = duty_cycle
		self.duration = duration


def save_picture(file_name):
	output_folder = "result/"

	print(f"Saving image {file_name} to {output_folder}{file_name}")
	
	# take picture

	#save picture


def configure_valve():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PWM_OUTPUT_PIN, GPIO.OUT)
	print(f"Configured valve on PWM pin {PWM_OUTPUT_PIN}")

def cleanup_valve():
	GPIO.cleanup()

def open_valve(setting):
	print(f"Running valve for {setting.duration} seconds")
	p = GPIO.PWM(PWM_OUTPUT_PIN, 0.5)
	p.start(1)
	time.sleep(setting.duration)
	p.stop()
	print("Valve closed")

def get_time_string():
	now = datetime.now()
	return now.strftime("%H:%M:%S")

def get_date_string():
	now = datetime.now()
	return now.strftime("%d-%m-%Y")

def main():
	FILENAME = "result/output.csv"
	camera = PiCamera()

	with open(FILENAME, 'w') as output_file:
		base_file_name = datetime.now().strftime("%Y%m%d_")
		
		print(f"Output file: {FILENAME}")

		configure_valve()

		print(f"Found {len(measurements)} measurments.")

		for n, meas in enumerate(measurements):
			print()
			print("Starting measurement with freq: {meas.frequency} duty cycle: {meas.dutycycle} for {meas.duration} seconds.")

			start_date = get_date_string()
			start_time = get_time_string()
			start_picture_name = f"{base_file_name}_{n}_start.png"
			stop_picture_name  = f"{base_file_name}_{n}_start.png"

			setting = Setting(meas[0],meas[1],VALVE_OPEN_TIME)
			
			print("Saving start image to 'result/{stop_picture_name}'")
			camera.capture('result/' + start_picture_name)
			
			open_valve(setting)

			print("Saving stop image to 'result/{stop_picture_name}'")
			camera.capture('result/' + stop_picture_name)

			print(f"Writing results of freq: {setting.frequency}, duty_cycle: {setting.dutycycle}, duration: {setting.duration}")

			output_file.write(start_date + "," + start_time + "," + \
						str(setting.frequency) + "," + setting.dutycycle + "," + setting.duration + "," + \
						start_picture_name + "," + stop_picture_name)

			print("Done.")

		print("Shutting down")
		cleanup_valve()

def test_camera():
	print("Test save picture")
	camera = PiCamera()
	camera.capture('result/' +"test.png")
	print("Done")

if __name__ == "__main__":
	test_camera()