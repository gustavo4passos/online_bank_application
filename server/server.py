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

# The server module is the entry of the server application.
# It supports multiple concurrent clients, serving each one
# in it's own thread and port.

import socket
import threading
import json

from _thread 		 import start_new_thread
from bank    		 import Bank
from logger  		 import Logger
from request_handler import handle_request
from client 		 import Client
from client 		 import NO_DATA
from datetime		 import datetime

# The name of the file which holds the state of the database
DATABASE_FILE_NAME = "database.json"
# The bank module is started before the server starts running
bank = Bank(DATABASE_FILE_NAME)

# Stores all event (requests and responses)
all_events_lock = threading.Lock()
all_events = []
# Current n of clients connected
n_clients_connected = 0

# Indicates if there a snapshot in progress
snapshot_in_progress_lock = threading.Lock()
snapshot_in_progress = False

next_snapshot_token = 1534

client_list = dict()
client_list_lock = threading.Lock()

def register_event(event):
	global all_events_lock
	global all_events
	all_events_lock.acquire()
	all_events.append(event)
	all_events_lock.release()

def create_snapshot():
	global next_snapshot_token
	global snapshot_in_progress 
	global client_list
	global client_list_lock
	snapshot_in_progress = True

	Logger.log_info('[SNAPSHOT] Snapshot thread started...')
	# Verify if all nodes have finished saving their state
	while True:
		snapshot_is_done = True
		# Because new clients may connect while the snapshot is being taken
		# the list is a critical section.
		client_list_lock.acquire()
		for id, client in client_list.items():
			if client.finished_saving_state() == False:
				snapshot_is_done = False
		client_list_lock.release()

		if snapshot_is_done:
			break

	Logger.log_info('[SHAPTHOT] All clients threads are done.')

	client_list_lock.acquire()
	for id, client in client_list.items():
		Logger.log_info(f'[SNAPSHOT] Channel {id}: {client.get_recorded_channel_messages()}')
		client.clear_channel_recorded_state()
	client_list_lock.release()
	
	snapshot_in_progress = False
	next_snapshot_token += 1
	Logger.log_info('Server finished saving state.')
	Logger.log_info('####################################')

def send_markers(token):
	for id, client in client_list.items():
		client.request_state_save()
		client.send(json.dumps({ 'type': 'save_state', 'token': token}).encode('ascii'))

# A client thread is created for each new client, which runs this
# function in a loop until the client disconnects or the connection 
# is lost.
def client_thread(connection, client_address, client):
	global snapshot_in_progress_lock
	global snapshot_in_progress
	global next_snapshot_token
	global all_events_lock
	global all_events
	global client_list

	while True:
		data = client.receive()

		if data:
			if data != NO_DATA:
				now = datetime.today()
				formatted_time = now.strftime("%H:%M:%S")

				register_event({f'request {client_address} {formatted_time}': data})

				decoded_data = data.decode('utf-8')
				response = handle_request(decoded_data, bank)


				# A node request that the server starts a snapshots
				if json.loads(response)["type"] == 'start_snapshot':
					snapshot_in_progress_lock.acquire()
					all_events_lock.acquire()
					Logger.log_info(f'############### SNAPSHOT {next_snapshot_token} ##############')
					Logger.log_info(f'[SNAPSHOT][EVENTS]')
					for item in all_events:
						Logger.log_info(f'[SNAPSHOT][EVENT] : {item} :')
					all_events.clear()
					all_events_lock.release()
					
					Logger.log_info(f'[SNAPSHOT] {bank.dump_database()}')
					if not snapshot_in_progress:
						snapshot_in_progress = True
						send_markers(next_snapshot_token)
						start_new_thread(create_snapshot, ())
					snapshot_in_progress_lock.release()

				# Some node sent a marker
				elif json.loads(response)["type"] == 'save_state':
					register_event({ f'response {client_address} {formatted_time}': response })
					# Mark this channel as finished
					if client.is_currently_saving_state():
						client.record_new_channel_message(decoded_data)
						client.send(data)
						client.finish_state_save()
					
				else:
					register_event({f'response {client_address} {formatted_time}': response})
					# If it's not a marker, record message
					if client.is_currently_saving_state():
						client.record_new_channel_message(decoded_data)
					client.send(response.encode('ascii'))
		else:
			client_list_lock.acquire()
			del client_list[client.id]
			client_list_lock.release()
			break

	Logger.log_info("Client on " + str(client_address) + " disconnected.")

	global n_clients_connected
	n_clients_connected -= 1
	Logger.log_info("Number of clients currently connected: {}.".format(n_clients_connected))
	
	connection.close()


def start_server():
	global n_clients_connected
	host = ""
	# The public default port for the server.
	port = 7069

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind(( host, port ))

	# Starts listening for new connection
	listening_socket.listen(5)

	global client_list
	global client_list_lock

	last_client_id = 0

	while True:
		# If a client connects to the server, start a new client 
		# thread and keep listening
		client_socket, client_address = listening_socket.accept()
		client_socket.setblocking(0)

		Logger.log_info("New client accepted on: " + str(client_address))
		n_clients_connected += 1
		Logger.log_info("Number of clients currently connected: {}.".format(n_clients_connected))

		last_client_id += 1
		new_client = Client(last_client_id, client_socket)
		
		client_list_lock.acquire()
		client_list[last_client_id] = new_client
		client_list_lock.release()

		start_new_thread(client_thread, (client_socket, client_address, new_client))

	listening_socket.close()

# Entry point
start_server()