import threading 

console_print_lock = threading.Lock()

class Logger:
	@staticmethod
	def log_info(text):
		console_print_lock.acquire()
		print("[INFO] " + text)
		console_print_lock.release()
	
	@staticmethod
	def log_error(text):
		console_print_lock.acquire()
		print("[ERROR] " + text)
