import socket
import json
from enum import Enum

class Connection:

    def __init__(self):
        host = '127.0.0.1'
    
        # Define the connection port
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

    def is_connected(self):
        return self.connection

    def is_logged_in(self):
        return self.logged_in

    def is_manager(self):
        return self.is_a_manager        

    def request_login(self, account, password):
        requisition = {}
        requisition['op'] = 'l'
        requisition['account'] = account
        requisition['password'] = password
        json_req = json.dumps(requisition)
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
        requisition = {}
        requisition['op'] = 's'
        requisition['account'] = account
        requisition['amount'] = amount
        requisition['token'] = self.token
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_deposit(self, account, amount):
        requisition = {}
        requisition['op'] = 'd'
        requisition['account'] = account
        requisition['amount'] = amount
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_transfer(self, account, destination_account, amount):
        requisition = {}
        requisition['op'] = 't'
        requisition['account'] = account
        requisition['destination_account'] = destination_account
        requisition['amount'] = amount
        requisition['token'] = self.token
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_client_info(self, account):
        requisition = {}
        requisition['op'] = 'g'
        requisition['account'] = account
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response

    def request_balance(self, account):
        requisition = {}
        requisition['op'] = 'b'
        requisition['account'] = account
        requisition['token'] = self.token
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response
        
    def request_create_account(self, account, identification, name, password, is_manager):
        requisition = {}
        requisition['op'] = 'c'
        requisition['account'] = account
        requisition['id'] = identification
        requisition['name'] = name
        requisition['password'] = password
        requisition['is_manager'] = is_manager
        requisition['token'] = self.token
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response
        
    def request_remove_account(self, account_to_remove, account):
        requisition = {}
        requisition['op'] = 'r'
        requisition['account_to_remove'] = account_to_remove
        requisition['account'] = account
        requisition['token'] = self.token
        json_req = json.dumps(requisition)
        self.socket.send(json_req.encode('ascii'))

        data = self.socket.recv(1024)
        response = json.loads(data)
        return response
        
                  


    
        
        