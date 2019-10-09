# Import socket module 
import socket
from enum import Enum
from bank_connection import Connection

is_logged_in = False
account_number = "0"
is_manager = False

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


def main(): 
    #connect
    connection = Connection()

    global is_logged_in
    global account_number
    global is_manager

    while True: 
        # read message to send to serve
        op = input('\nOperacao: ')
        if op == 'quit': 
            break
        
        if(op == 'l'):
            account = input('Conta: ')
            password = input('Senha: ')
            status = connection.request_login(account, password)
            if status["type"] != "login_success":
                print("Não foi possível fazer o login.{}".format(get_error_message(status)))
            else:
                is_logged_in = True
                account_number = account
                is_manager = status["is_manager"]

                print("Bem vindo, {}! Você está logado.".format(status["name"]))

        elif(op == 'd'):
            account = input('Conta destino: ')
            amount = input('Valor: ')
            status = connection.request_deposit(account, amount)

            if status["type"] != "ok":
                print("Não possível realizar o depósito. {}".format(get_error_message(status)))
            else:
                print("Depósito efetuado com sucesso.")
            
        elif(op == 's'):
            if(not is_logged_in):
                print("Operação inválida")
            else:    
                amount = input('Valor: ')
                status = connection.request_withdrawal(account_number, amount)
                if status["type"] != "ok":
                    print("Não possível realizar o saque. {}".format(get_error_message(status)))
                else:
                    print("Saque efetuado com sucesso.")

        elif(op == 't'):
            if(not is_logged_in):
                print("Operação inválida")
            else:    
                destination_account = input('Conta favorecida: ')
                
                status = connection.request_client_info(destination_account)
                if(status["type"] != "account_info"):
                    print("Conta inválida.")
                    continue
        
                option = input("Nome do destinatário {}. Confirma? s/n".format(status["name"]))
                if option != "s":
                    continue

                amount = input('Valor: ')
                status = connection.request_transfer(account, destination_account, amount)
                if status["type"] == "ok":
                    print("Despósito efetuado com sucesso.")
                else:
                    print("Não foi possível realizar o depósito. {}.".format(get_error_message(status)))
            
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
                account_to_remove = input('Número da conta a ser removida:' )
                option = input("Tem certeza que quer remover a conta {}? s/n".format(account_to_remove))
                if option != 's':
                    continue

                status = connection.request_remove_account(account_to_remove, account_number)
                if(status["type"] != "ok"):
                    print("Não foi possível remover a conta. {}.".format(get_error_message(status)))
                else:
                    print("Conta removida com sucess.")

        elif(op == 'q'):
            print("Obrigado. Até a próxima!")
            break

        elif(op == 'o'):
            if not is_logged_in:
                print("Operação inválida.")
            else:
                is_logged_in = False
                account_number = ""
                is_manager = False
                print("Você foi desconectado com sucesso.")

        else:
            print("Operação inválida.")            
        
main() 