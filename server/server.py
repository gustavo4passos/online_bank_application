import socket
import threading
import json

from bank import Bank

from _thread import *

bank = Bank("database.json")

def client_thread(connection):
	while True:
		data = connection.recv(1024)
		if not data:
			return

	print("Client closed")
	connection.close()

def start_server():
	host = ""
	port = 7049

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.bind(( host, port ))

	listening_socket.listen(5)

	while True:
		client_socket, client_address = listening_socket.accept();	
		print("New client accepted. Ip: " + str(client_address))

		start_new_thread(client_thread, (client_socket, ))
	listening_socket.close();

start_server()
