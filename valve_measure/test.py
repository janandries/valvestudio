import time
from datetime import datetime

def get_now_date():
	now = datetime.now()
	return now.strftime("%Y%m%d")

def get_now_time():
	now = datetime.now()
	return now.strftime("%H%M%S")

FILENAME = f"result/{get_now_date()}_{get_now_time()}_output.csv"

print(FILENAME)
