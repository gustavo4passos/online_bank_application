# Import socket module 
import socket
from enum import Enum
from bankConnection import Connection

  
def Main(): 
    #connect
    connection = Connection()
    print(connection.is_connected())

    while True: 
  
        # read message to send to serve
        op = input('\nOperacao: ')
        if op == 'quit': 
            break
        

        if(op == 'l'):
            account = input('Conta: ')
            password = input('Senha: ')
            connection.request_login(account, password)
            
        elif(op == 'd'):
            account = input('Conta: ')
            amount = input('Valor: ')
            connection.request_deposit(account, amount)
            
        elif(op == 's'):
            account = input('Conta: ')
            amount = input('Valor: ')
            connection.request_withdrawal(account, amount)

        elif(op == 't'):
            account = input('Conta: ')
            destination_account = input('Conta favorecida: ')
            amount = input('Valor: ')
            connection.request_transfer(account, destination_account, amount)
            
        elif(op == 'g'):
            account = input('Conta: ')
            connection.request_client_info(account)

        elif(op == 'b'):
            account = input('Conta:' )
            connection.request_balance(account)

        elif(op == 'c'):
            account = input('Conta:' )
            id = input('RG:' )
            name = input('Nome:' )
            password = input('Password:' )
            manager = input('Administrador: S/N' )
            if(manager == 'S'):
                is_manager = True
            else:
                is_manager = False
            
            connection.request_create_account(account, id, name, password, is_manager)

        elif(op == 'r'):
            account_to_remove = input('Conta a ser removida:' )
            account = input('Conta:' )
            connection.request_remove_account(account_to_remove, account)             

   

    
        #answer = answer.split('/')
        #if(answer[0] == "OK"):
        #    print("Success")
        #elif(answer[0] == "BALANCE"):
        #    print("Saldo = " + str(answer[2]))    
        #elif(answer[0] == "INVALID_ACCOUNT"):
        #    print("Invalide acount, please create one")
        #elif(answer[0] == "INVALID_DESTINATION_ACCOUNT"):
        #    print("Destination account doesn't exist")
        #elif(answer[0] == "INVALID_AMOUNT"):
        #    print("Invalid amount")
        #elif(answer[0] == "BAD_REQUEST"):
        #    print("BAD REQUEST")                
        
   
  
if __name__ == '__main__': 
    Main() 