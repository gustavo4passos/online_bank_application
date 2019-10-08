# Import socket module 
import socket
from enum import Enum
from bankConnection import Connection

  
def Main(): 
    #connect
    connection = Connection()

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
            if(connection.is_logged_in == False):
                print('Operação necessita de login')
            account = input('Conta: ')
            amount = input('Valor: ')
            connection.request_withdrawal(account, amount)

        elif(op == 't'):
            if(connection.is_logged_in() == False):
                print('Operação necessita de login')
            account = input('Conta: ')
            destination_account = input('Conta favorecida: ')
            amount = input('Valor: ')
            connection.request_transfer(account, destination_account, amount)
            
        elif(op == 'g'):
            account = input('Conta: ')
            connection.request_client_info(account)

        elif(op == 'b'):
            if(connection.is_logged_in() == False):
                print('Operação necessita de login')
            account = input('Conta:' )
            connection.request_balance(account)

        elif(op == 'c'):
            if(connection.is_logged_in() == False):
                print('Operação necessita do login administrador')
            account = input('Conta:' )
            id = input('RG: ' )
            name = input('Nome: ' )
            password = input('Password: ' )
            manager = input('Administrador? S/N: ' )
            if(manager == 'S'):
                is_manager = True
            else:
                is_manager = False
            
            connection.request_create_account(account, id, name, password, is_manager)

        elif(op == 'r'):
            if(connection.is_logged_in() == False):
                print('Operação necessita do login administrador')
            account_to_remove = input('Conta a ser removida:' )
            account = input('Conta:' )
            connection.request_remove_account(account_to_remove, account)                    
        
   
  
if __name__ == '__main__': 
    Main() 