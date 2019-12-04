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
import threading

from enum    import Enum
from _thread import start_new_thread

class BankConnection:    
    def __init__(self):
        host = '127.0.0.1'
    
        # Port the server is listening at
        port = 7069
    
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    
        # connect to server
        self.logged_in = False 
        self.connection = True
        self.is_a_manager = False

        self.is_saving_state = False
        self.responses = []
        self.pending_requests = []
        self.responses_queue = []

        self.all_events_lock = threading.Lock()
        self.all_events = []

        try:
            s.connect((host,port)) 
            self.socket = s
            self.socket.setblocking(0)
            #start_new_thread(self.handle_connection, self)
            t1 = threading.Thread(target = self.handle_connection)
            t1.start()

        except socket.timeout:
            self.connection = False

    def save_state(self, token):
        print('[SNAPSHOT][STATE]')
        state = vars(self)
        print(f'Snapshot token: {token}')
        print('Channel 0: Empty \n')
        print('\n'.join(f'{key}: {value}' for key, value in state.items()))
        print('\n')

    def handle_request(self, request):
        self.all_events_lock.acquire()
        self.all_events.append({ 'request': request})
        self.all_events_lock.release()

        self.pending_requests.append(request.encode('ascii'))

        while(self.has_response() != True):
            pass

        response = self.responses[0]
        self.responses.remove(response)

        return response             
            

    def handle_connection(self):
        while(self.connection):
            if(len(self.pending_requests) != 0):
                self.socket.send(self.pending_requests[0])
                self.pending_requests.pop(0)

            NO_DATA = -1
            try:
                data = self.socket.recv(1024)
            except:
                data = NO_DATA

            if data:
                if data != NO_DATA:   
                    self.all_events_lock.acquire()
                    self.all_events.append({ 'response': data })
                    self.all_events_lock.release()

                    response = json.loads(data)
                    if(response["type"] == "save_state"):
                        # Finish snapshot
                        if(self.is_saving_state):
                            print('[SNAPSHOT][CHANNEL]')
                            print(self.responses_queue)
                            self.responses_queue.clear()
                            print('#########################################################')
                            self.is_saving_state = False
                        else:
                            # Start saving state
                            print(f'\n################### SNAPSHOT {response["token"]} ###################')
                            self.all_events_lock.acquire()
                            print(f'[SNAPSHOT][EVENTS]')
                            print(self.all_events)
                            self.all_events.clear()
                            self.all_events_lock.release()
                            self.socket.send(json.dumps(response).encode('ascii'))
                            self.save_state(response["token"])
                            self.is_saving_state = True
                    else:
                        self.responses.append(response)     

                    if(self.is_saving_state == True):
                        self.responses_queue.append(response)
            else:
                break
                    

    def close_connection(self):
        self.connection = False                 

    def is_manager(self):
        return self.is_a_manager   

    def has_response(self):
        if(len(self.responses) != 0):
            return True
        return False        

    def request_login(self, account, password):
        request = {}
        request['op'] = 'l'
        request['account'] = account
        request['password'] = password
        json_req = json.dumps(request)

        response = self.handle_request(json_req)

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

        return self.handle_request(json_req)

    

    def request_deposit(self, account, amount):
        request = {}
        request['op'] = 'd'
        request['account'] = account
        request['amount'] = amount
        json_req = json.dumps(request)

        return self.handle_request(json_req)

    def request_transfer(self, account, destination_account, amount):
        request = {}
        request['op'] = 't'
        request['account'] = account
        request['destination_account'] = destination_account
        request['amount'] = amount
        request['token'] = self.token
        json_req = json.dumps(request)
        
        return self.handle_request(json_req)

    def request_client_info(self, account):
        request = {}
        request['op'] = 'g'
        request['account'] = account
        json_req = json.dumps(request)

        return self.handle_request(json_req)

    def request_balance(self, account):
        request = {}
        request['op'] = 'b'
        request['account'] = account
        request['token'] = self.token
        json_req = json.dumps(request)

        return self.handle_request(json_req)
      
        
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

        return self.handle_request(json_req)
        
    def request_remove_account(self, account_to_remove, account):
        request = {}
        request['op'] = 'r'
        request['account_to_remove'] = account_to_remove
        request['account'] = account
        request['token'] = self.token
        json_req = json.dumps(request)

        return self.handle_request(json_req)

    def request_snapshot(self):
        request = {}
        request['op'] = 'start_snapshot'
        json_req = json.dumps(request)
        self.socket.send(json_req.encode('ascii'))