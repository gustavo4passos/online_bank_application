import socket
import os
import datetime
from enum import Enum
from bank_connection import Connection

is_logged_in = False
account_number = "0"
is_manager = False
client_name = "invalid_name"

def get_error_message(operation_status):
    type = operation_status["type"]
    if type == "wrong_password":
        return "Senha incorreta."
    if type == "invalid_account":
        return "Conta inválida."
    if type == "invalid_amount":
        return "Quantia inválida"
    if type == "non_sufficient_funds":
        return "Saldo insuficiente"
    if type == "invalid_token":
        return "Token inválido."
    # This should never be hit
    if type == "bad_request":
        return "Fatal: O formato da requisição é invalido"


default_operations = [ 
    "Entrar na sua conta - l", 
    "Depósito - d", 
    "Mostrar operações - m",
    "Sair - q"]

client_operations = [ 
    "Saldo - b",
    "Depósito - d", 
    "Transferência - t",
    "Mostrar operações - m",
    "Desconectar - o",
    "Sair - q"]

manager_operations = [ 
    "Saldo - b",
    "Depósito - d", 
    "Transferência - t",
    "Criar conta - c",
    "Remover conta - r",
    "Mostrar operações - m",
    "Desconectar - o",
    "Sair - q"]

def get_greeting_message():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour <= 12:
        return "Bom dia"
    elif hour <= 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def display_available_operations():
    if(not is_logged_in):
        for operation in default_operations:
            print(operation)
    elif(not is_manager):
        for operation in client_operations:
            print(operation)
    else:
        for operation in manager_operations:
            print(operation)

def display_greeting():
    print("{}{}{}".format(get_greeting_message(), ", " + client_name if is_logged_in  else "", "!"))

def is_amount_valid(amount):
    try:
        float(amount)
    except:
        return False
    if float(amount) < 0:
        return False
    return True

def run(): 
    connection = Connection()

    global is_logged_in
    global account_number
    global is_manager
    global client_name

    display_greeting()
    display_available_operations()

    while True: 
        op = input('\nOperação (m para ver opções): ')
        if op == 'q': 
            display_greeting()
            print("Até a próxima!")
            break
        
        if(op == 'l'):
            if(is_logged_in):
                print("Operação inválida.")
            else:
                print("\nLogin.")
                account = input('Conta: ')
                password = input('Senha: ')
                status = connection.request_login(account, password)
                if status["type"] != "login_success":
                    print("Não foi possível fazer o login. {}".format(get_error_message(status)))
                else:
                    is_logged_in = True
                    account_number = account
                    is_manager = status["is_manager"]
                    client_name = status["name"]

                    print("Bem vindo, {}! Você está logado.".format(client_name))

        elif(op == 'd'):
            print("\nDepósito.")
            account = input('Conta destino: ')

            info = connection.request_client_info(account)
            if(info["type"] != "account_info"):
                print("Conta inválida.")
            else:
                option = input("Nome do destinatário: {}. Confirma? s/n: ".format(info["name"]))
                if option != 's':
                    print("Operação cancelada.")
                else:
                    amount = input('Valor: ')
                    if not is_amount_valid(amount):
                        print("Valor inválido.")
                    else:
                        status = connection.request_deposit(account, float(amount))
                        if status["type"] != "ok":
                            print("Não possível realizar o depósito. {}".format(get_error_message(status)))
                        else:
                            print("Depósito efetuado com sucesso.")
                    
        elif(op == 's'):
            if(not is_logged_in):
                print("Operação inválida")
            else:    
                print("\nSaque.")
                amount = input('Valor: ')
                if not is_amount_valid(amount):
                    print("Valor inválido.")
                else:   
                    status = connection.request_withdrawal(account_number, float(amount))
                    if status["type"] != "ok":
                        print("Não possível realizar o saque. {}".format(get_error_message(status)))
                    else:
                        print("Saque efetuado com sucesso.")

        elif(op == 't'):
            if(not is_logged_in):
                print("Operação inválida")
            else:    
                print("\nTransferência")
                destination_account = input('Conta favorecida: ')
                status = connection.request_client_info(destination_account)
                if(status["type"] != "account_info"):
                    print("Conta inválida.")
                    continue
        
                option = input("Nome do destinatário: {}. Confirma? s/n: ".format(status["name"]))
                if option != "s":
                    continue

                amount = input('Valor: ')
                if(not is_amount_valid(amount)):
                    print("Valor inválido.")
                else:
                    status = connection.request_transfer(account, destination_account, float(amount))
                    if status["type"] == "ok":
                        print("Transferência efetuada com sucesso.")
                    else:
                        print("Não foi possível realizar a Transferência. {}.".format(get_error_message(status)))
                
        elif(op == 'b'):
            if(not is_logged_in):
                print("Operação inválida")
            else:    
                status = connection.request_balance(account_number)
                if status["type"] != "balance":
                    print("Não foi possível acessar o seu saldo. {}".format(get_error_message(status)))
                else:
                    print("Saldo disponível: R$ {}".format(status["balance"]))

        elif(op == 'c'):
            if(not is_logged_in or not is_manager):
                print("Operação inválida.")
            else:    
                print("\nCriar nova conta.")
                id = input('RG: ' )
                name = input('Nome: ' )
                password = input('Password: ' )
                manager = input('Conta de gerente? s/n: ' )
                if(manager == 's'):
                    is_manager_account = True
                else:
                    is_manager_account = False
                
                status = connection.request_create_account(account, id, name, password, is_manager_account)
                
                if(status["type"] != "account_created"):
                    print("Não foi possível criar a conta. {}.".format(get_error_message(status)))
                else:
                    print("Conta criada com sucesso! Número da nova conta: {}.".format(status["account"]))

        elif(op == 'r'):
            if(not is_manager or not is_logged_in):
                print("Operação inválida.")
            else:    
                print("\nRemover conta.")
                account_to_remove = input('Número da conta a ser removida: ' )
                option = input("Tem certeza que quer remover a conta {}? s/n: ".format(account_to_remove))
                if option != 's':
                    continue

                status = connection.request_remove_account(account_to_remove, account_number)
                if(status["type"] != "ok"):
                    print("Não foi possível remover a conta. {}.".format(get_error_message(status)))
                else:
                    print("Conta removida com sucesso.")

        elif(op == 'o'):
            if not is_logged_in:
                print("Operação inválida.")
            else:
                is_logged_in = False
                account_number = ""
                is_manager = False
                client_name = "invalid_name"
                print("Você foi desconectado com sucesso.")

        elif(op == 'm'):
            print('')      
            display_available_operations()

        else:
            print("Operação inválida.")      
        
run()