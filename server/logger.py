import threading 
from datetime import datetime

console_print_lock = threading.Lock()

class Logger:
	@staticmethod
	def log_info(text):
		console_print_lock.acquire()
		now = datetime.today()
		formatted_time = now.strftime("%H:%M:%S")
		print("[INFO](" + formatted_time + "): " + text)
		console_print_lock.release()
	
	@staticmethod
	def log_error(text):
		console_print_lock.acquire()
		print("[ERROR] " + text)
