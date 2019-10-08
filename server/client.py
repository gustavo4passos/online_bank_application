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
        s.send('{ "op": "t", "account": "3584", "token": "trefssim", "destination_account": "3579", "amount": 16 }'.encode('ascii'))
  
        # messaga received from server 
        data = s.recv(1024) 
  
        # print the received message 
<<<<<<< HEAD
        print('Received from the server :',str(data.decode('ascii'))) 
=======
        # here it would be a reverse of sent message 
        print('Received from the server :',str(data.decode('utf-8'))) 
        break
>>>>>>> e8c90fb321a5251acc0bf5cbbf2e1c6dd9b183c2
  
        # ask the client whether he wants to continue 
        
    # close the connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 