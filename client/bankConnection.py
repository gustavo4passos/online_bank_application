import socket
from enum import Enum

class Connection:

    def __init__(self):
        host = '127.0.0.1'
    
        # Define the connection port
        port = 7049
    
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
        # connect to server 
        self.connection = True
        try:
            s.connect((host,port)) 
            self.socket = s

        except socket.timeout:
            self.connection = False  

    def is_connected(self):
        return self.connection

    def request_withdrawal(self, account, amount):
        return True

    def request_deposit(self, account, amount):
        return True

    def request_transfer(self, account, destination_acount, amount):
        return True

    def request_client_info(self, account):
        return True

    def request_balance(self, account):
        return True

    def request_login(self, account, password):
        return True

    def request_create_account(self, account, id, name, password, is_manager):
        return True

    def request_remove_account(self, account_to_remove, account):
        return True                            


    
        
        