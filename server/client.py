import threading

# Constant to represent no data has been received
NO_DATA = -1

class Client(object):
	def __init__(self, id, connection):
		self.socket_access_lock = threading.Lock()
		self.connection 	   = connection
		self.id 			   = id
		self.pending_requests  = []
		self.pending_responses = []
		self.is_saving_state   = False
		self.channel_state     = []
	
	def send(self, message):
		self.socket_access_lock.acquire()
		self.connection.send(message)
		self.socket_access_lock.release()

	def receive(self):
		self.socket_access_lock.acquire()
		try:
			data = self.connection.recv(1024)
		except:
			data = NO_DATA
		self.socket_access_lock.release()

		return data

	def is_currently_saving_state(self):
		return self.is_saving_state

	def request_state_save(self):
		self.is_saving_state = True

	def finish_state_save(self):
		self.is_saving_state = False
	
	def finished_saving_state(self):
		return not self.is_saving_state

	def record_new_channel_message(self, message):
		self.channel_state.append(message)

	def clear_channel_recorded_state(self):
		self.channel_state.clear()

	def get_recorded_channel_messages(self):
		return self.channel_state
