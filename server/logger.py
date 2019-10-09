#####################################################
#												   	#
#	Universidade Federal da Bahia		   		   	#
#	Fundamentos de Sistemas Distribuidos		   	#
# 												   	#
#	Gustavo Passos								   	#
#	Daniel Lopes								   	#
# 	Alisson Souza								   	#
#												   	#
#####################################################

# A thread safe logger.
# Does simple messaging logging (with error or info) prefixes, 
# including a time stamp
# Logger is a static class, and should NOT be instantiated.

import threading 
from datetime import datetime

# Logging mutex
console_print_lock = threading.Lock()

class Logger:
	# Log info message to the console
	@staticmethod
	def log_info(text):
		console_print_lock.acquire()
		now = datetime.today()
		formatted_time = now.strftime("%H:%M:%S")
		print("[INFO](" + formatted_time + "): " + text)
		console_print_lock.release()
	
	# Log error message to the console
	@staticmethod
	def log_error(text):
		console_print_lock.acquire()
		print("[ERROR] " + text)
