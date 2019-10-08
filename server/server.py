import socket
import threading
import json

from _thread 		 import start_new_thread
from bank    		 import Bank
from logger  		 import Logger
from request_handler import handle_request

DATABASE_FILE_NAME = "database.json"
bank = Bank(DATABASE_FILE_NAME)
 
def client_thread(connection, client_address):
	while True:
		data = connection.recv(1024)
		decoded_data = data.decode('utf-8')
		if not data:
			break

		response = handle_request(decoded_data, bank)
		connection.send(response.encode('ascii'))

	Logger.log_info("Client on " + str(client_address) + " disconnected.")
	connection.close()

def start_server():
	host = ""
	port = 7049

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind(( host, port ))

	listening_socket.listen(5)

	while True:
		client_socket, client_address = listening_socket.accept()
		Logger.log_info("New client accepted on: " + str(client_address))
		start_new_thread(client_thread, (client_socket, client_address))

	listening_socket.close()

start_server()