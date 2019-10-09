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

# This module exposes the functionaliaty provided by the bank server
# to the client through the network.
# It's responsible for connecting to the server, sending requests
# over the netork and delivering the response.

import socket
import json
from enum import Enum

class BankConnection:

    def __init__(self):
        host = '127.0.0.1'
    
        # Port the server is listening at
        port = 7049
    
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
        # connect to server
        self.logged_in = False 
        self.connection = True
        self.is_a_manager = False

        try:
            s.connect((host,port)) 
            self.socket = s

        except socket.timeout:
            self.connection = False  

    def is_manager(self):
        return self.is_a_manager        

    def request_login(self, account, password):
        request = {}
        request['op'] = 'l'
        request['account'] = account
        request['password'] = password
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))
        data = self.socket.recv(1024)
        response = json.loads(data)

        if(response["type"] == "login_success"):
            self.token = response["token"]
            self.logged_in = True
            if(response["is_manager"] == True):
                self.is_a_manager = True
        
        return response

    def request_withdrawal(self, account, amount):
        request = {}
        request['op'] = 's'
        request['account'] = account
        request['amount'] = amount
        request['token'] = self.token
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_deposit(self, account, amount):
        request = {}
        request['op'] = 'd'
        request['account'] = account
        request['amount'] = amount
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_transfer(self, account, destination_account, amount):
        request = {}
        request['op'] = 't'
        request['account'] = account
        request['destination_account'] = destination_account
        request['amount'] = amount
        request['token'] = self.token
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_client_info(self, account):
        request = {}
        request['op'] = 'g'
        request['account'] = account
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_balance(self, account):
        request = {}
        request['op'] = 'b'
        request['account'] = account
        request['token'] = self.token
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response
        
    def request_create_account(self, account, identification, name, password, is_manager):
        request = {}
        request['op'] = 'c'
        request['account'] = account
        request['id'] = identification
        request['name'] = name
        request['password'] = password
        request['is_manager'] = is_manager
        request['token'] = self.token
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response
        
    def request_remove_account(self, account_to_remove, account):
        request = {}
        request['op'] = 'r'
        request['account_to_remove'] = account_to_remove
        request['account'] = account
        request['token'] = self.token
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response