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

    def request_withdrawal(self, account, password):
        return True


    
        
        