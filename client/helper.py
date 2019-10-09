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

# Returns a descriptive error message from an error response
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
        return "Token inválido"
    # This should never be hit
    if type == "bad_request":
        return "Fatal: O formato da requisição é invalido"

# Checks if amount is valid (int or fload and > 0)
def is_amount_valid(amount):
    try:
        float(amount)
    except:
        return False
    if float(amount) < 0:
        return False
    return True