# Import socket module 
import socket 
  
  
def Main(): 
    # local host IP '127.0.0.1' 
    host = '127.0.0.1'
  
    # Define the port on which you want to connect 
    port = 7049
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host,port)) 
  
    # message you send to server 
    while True: 
  
        # # message sent to server
        # allMessage = ''
        # message = input('\nName: ')
        # if message == 'quit': 
        #     break
        # allMessage += message+'/'
        # message = input('Operation: ')
        # allMessage += message+'/'
        # message = input('Valor: ')
        # allMessage += message
        
        # s.send(allMessage.encode('ascii')) 
        # s.send('{ "op": "c", "account": "3579", "id": "03124567", "name": "Marciano Quatro", "password": "tressim", "token": "12345", "is_manager": false }'.encode('ascii'))
        # s.send('{ "op": "l", "account": "3584", "password": "tressim" }'.encode('ascii'))
        # s.send('{ "op": "t", "account": "3584", "token": "trefssim", "destination_account": "3579", "amount": 16 }'.encode('ascii'))
        s.send('{ "op": "g", "account": "3584"}'.encode('ascii'))
        # s.send('{ "op": "r", "account_to_remove": "3584", "token": "12345", "account": "3579" }'.encode('ascii'))

  
        # messaga received from server 
        data = s.recv(1024) 
  
        # print the received message 
        # here it would be a reverse of sent message 
        print('Received from the server :',str(data.decode('utf-8'))) 
        break
  
        # ask the client whether he wants to continue 
        
    # close the connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 