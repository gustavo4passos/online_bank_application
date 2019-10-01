# Import socket module 
import socket
from enum import Enum

  
def Main(): 
    # local host IP '127.0.0.1' 
    host = '127.0.0.1'
  
    # Define the port on which you want to connect 
    port = 12345
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server 
    s.connect((host,port)) 
    while True: 
  
        # read message to send to server
        allMessage = ''
        message = input('\nOperacao: ')
        if message == 'quit': 
            break
        allMessage += message+'/'

        if(message == 'l'):
            message = input('Conta: ')
            allMessage += message+'/'
            message = input('Senha: ')
            allMessage += message+'/'
        elif(message == 'd'):
            message = input('Conta: ')
            allMessage += message+'/'
            message = input('Valor: ')
            allMessage += message+'/'
        elif(message == 's'):
            message = input('Conta: ')
            allMessage += message+'/'
            message = input('Valor: ')
            allMessage += message+'/'
        elif(message == 't'):
            message = input('Conta: ')
            allMessage += message+'/'
            message = input('Conta favorecida: ')
            allMessage += message+'/'
            message = input('Valor: ')
            allMessage += message+'/'
        elif(message == 'c'):
            message = input('Conta: ')
            allMessage += message+'/'

        allMessage += message+'\r\n'   

        s.send(allMessage.encode('ascii'))
  
        # receive message from server 
        data = s.recv(1024)

        answer = data.decode('ascii')
        answer = answer.split('/')
        if(answer[0] == "OK"):
            print("Success")
        elif(answer[0] == "BALANCE"):
            print("Saldo = " + str(answer[2]))    
        elif(answer[0] == "INVALID_ACCOUNT"):
            print("Invalide acount, please create one")
        elif(answer[0] == "INVALID_DESTINATION_ACCOUNT"):
            print("Destination account doesn't exist")
        elif(answer[0] == "INVALID_AMOUNT"):
            print("Invalid amount")
        elif(answer[0] == "BAD_REQUEST"):
            print("BAD REQUEST")                
        
        
    # finish connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 