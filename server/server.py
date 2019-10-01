import socket
import threading
import json

from _thread import *
from bank import Bank

global bank 

def client_thread(connection, client_address):
	while True:
		data = connection.recv(1024)
		if not data:
			break

	print("Client on " + str(client_address) + " disconnected.")
	connection.close()

def start_server():
	bank = Bank("database.json")
	hos = ""
	port = 7049

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind(( host, port ))

	listening_socket.listen(5)

	while True:
		client_socket, client_address = listening_socket.accept();	
		print("New client accepted on: " + str(client_address))

		start_new_thread(client_thread, (client_socket, client_address))
	listening_socket.close();

start_server()
