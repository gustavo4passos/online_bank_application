# Import socket module 
import socket
from enum import Enum
from bankConnection import Connection



def Main():
    first_manager = False
    first_login = False 
    is_logged_in = False
    is_manager = False      
    #connect
    connection = Connection()
    if(connection.is_connected() == True):
        print('Sistema iniciado, operações sem login: ')
        print('Login - l\nDeposito - d\nConsultar cliente - g\nSair - quit')
    while True: 
        # read message to send to serve
        if(is_logged_in == True and first_login == False):
            print('\nUsuário logado, operações possíveis: ')
            print('Saque - s\nTransferência - t\nConsultar saldo - b\n')
            first_login = True
        if(is_logged_in == True and is_manager == True and  first_manager == False):
            print('Operações de administrador: ')
            print('Criar conta - c\nRemover conta - r\n')
            first_manager = True    

        op = input('\nOperacao: ')
        if op == 'quit': 
            break
        
        if(op == 'l'):
            account = input('Conta: ')
            password = input('Senha: ')
            connection.request_login(account, password)
            is_logged_in = True
            is_manager = True

            
        elif(op == 'd'):
            account = input('Conta: ')
            amount = input('Valor: ')
            connection.request_deposit(account, amount)
            
        elif(op == 's'):
            if(connection.is_logged_in() == False):
                print('Operação necessita de login')
            else:    
                account = input('Conta: ')
                amount = input('Valor: ')
                connection.request_withdrawal(account, amount)

        elif(op == 't'):
            if(connection.is_logged_in() == False):
                print('Operação necessita de login')
            else:    
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
            else:    
                account = input('Conta:' )
                connection.request_balance(account)

        elif(op == 'c'):
            if(connection.is_logged_in() == False):
                print('Operação necessita do login administrador')
            else:    
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
            else:    
                account_to_remove = input('Conta a ser removida:' )
                account = input('Conta:' )
                connection.request_remove_account(account_to_remove, account)                    
        
   
  
if __name__ == '__main__': 
    Main() 