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

# The name of the file which holds the state of the database
DATABASE_FILE_NAME = "database.json"
# The bank module is started before the server starts running
bank = Bank(DATABASE_FILE_NAME)

# Current n of clientes connected
n_clients_connected = 0

# A client thread is created for each new client, which runs this
# function in a loop until the client disconnects or the connection 
# is lost.
def client_thread(connection, client_address):
	while True:
		data = connection.recv(1024)
		decoded_data = data.decode('utf-8')
		if not data:
			break

		response = handle_request(decoded_data, bank)
		connection.send(response.encode('ascii'))

	Logger.log_info("Client on " + str(client_address) + " disconnected.")

	global n_clients_connected
	n_clients_connected -= 1
	Logger.log_info("Number of clients currently connected: {}.".format(n_clients_connected))
	
	connection.close()

def start_server():
	global n_clients_connected
	host = ""
	# The public default port for the server.
	port = 7049

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind(( host, port ))

	# Starts listening for new connection
	listening_socket.listen(5)

	while True:
		# If a client connects to the server, start a new client 
		# thread and keep listening
		client_socket, client_address = listening_socket.accept()
		Logger.log_info("New client accepted on: " + str(client_address))
		n_clients_connected += 1
		Logger.log_info("Number of clients currently connected: {}.".format(n_clients_connected))
		start_new_thread(client_thread, (client_socket, client_address))

	listening_socket.close()

# Entry point
start_server()