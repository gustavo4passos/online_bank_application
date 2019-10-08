import json
from bank   import ERROR_TYPE
from logger import Logger
from enum   import Enum

def handle_request(request, bank):
    request_obj = { }
    try:
        request_obj = json.loads(request)
    except:
        return create_bad_request_response("Request is not valid json")

    if not assert_types(request_obj):
        return create_bad_request_response("Type mismatch.")
    elif("op" not in request_obj):
        return create_bad_request_response("Request is missing operation specifier.")
    
    op = request_obj['op']
    if op == 's':
        return handle_request_withdraw(request_obj, bank)
    elif op == 'l':
        return handle_request_login(request_obj, bank)
    elif op == 'd':
        return handle_request_deposit(request_obj, bank)
    elif op == 'c':
        return handle_request_create_account(request_obj, bank)
    elif op == 'b':
        return handle_request_get_balance(request_obj, bank)
    elif op == 't':
        return handle_request_transfer(request_obj, bank)
    elif op == 'g':
        return handle_request_get_owner_name(request_obj, bank)
    elif op == 'r':
        return handle_request_remove_account(request_obj, bank)
    else:
        return create_bad_request_response("Unknown operation")

def handle_request_withdraw(request_obj, bank):
    if "account" in request_obj and "amount" in request_obj and "token" in request_obj:
        account = request_obj["account"]
        amount  = request_obj["amount"]
        token   = request_obj["token"]

        bank_response = bank.withdraw(account, amount, token)
        return handle_default_response(bank_response)
    else:
        return create_bad_request_response()

def handle_request_login(request_obj, bank):
    if "account" in request_obj and "password" in request_obj:
        account  = request_obj["account" ]
        password = request_obj["password"]
        bank_response = bank.login(account, password)

        if(bank_response["status"] != ERROR_TYPE.NO_ERROR):
            return create_error_response(bank_response)
        else:
            name       = bank_response["data"]["name"      ]
            token      = bank_response["data"]["token"     ]
            balance    = bank_response["data"]["balance"   ]
            is_manager = bank_response["data"]["is_manager"]

            return json.dumps({ 
                "type": "login_success", 
                "name": name, 
                "balance": balance,
                "is_manager": is_manager, 
                "token": token
            })
    else:
        return create_bad_request_response()
    

def handle_request_deposit(request_obj, bank):
    if "account" in request_obj and "amount" in request_obj:
        account = request_obj["account"]
        amount  = request_obj["amount" ]

        bank_response = bank.deposit(account, amount)
        return handle_default_response(bank_response)

    else:
        return create_bad_request_response()

def handle_request_transfer(request_obj, bank):
    if "account" in request_obj and "destination_account" in request_obj and "amount" in request_obj and "token" in request_obj:
        account             = request_obj["account"]
        destination_account = request_obj["destination_account"]
        amount              = request_obj["amount"]
        token               = request_obj["token"]

        bank_response = bank.transfer(account, destination_account, amount, token)
        return handle_default_response(bank_response)
        
    else:
        return create_bad_request_response()


def handle_request_create_account(request_obj, bank):
    if "account" in request_obj and "id" in request_obj and "name" in request_obj and "password" in request_obj and "token" in request_obj and "is_manager" in request_obj:
        account         = request_obj["account"   ]
        identification  = request_obj["id"        ]
        name            = request_obj["name"      ]
        password        = request_obj["password"  ]
        token           = request_obj["token"     ]
        is_manager      = request_obj["is_manager"]

        bank_response = bank.create_account(identification, name, password, account, is_manager, token)
        if bank_response["status"] != ERROR_TYPE.NO_ERROR:
            return create_error_response(bank_response)
        else:
            return json.dumps({
                "type": "account_created",
                "account": bank_response["data"]
            })   
    else:
        return create_bad_request_response()

def handle_request_get_balance(request_obj, bank):
    if "account" in request_obj and "token" in request_obj:
        account = request_obj["account"]
        token   = request_obj["token"  ]
        
        bank_response = bank.get_balance(account, token)
        if bank_response["status"] != ERROR_TYPE.NO_ERROR:
            return create_error_response(bank_response)
        else:
            return json.dumps({ "type": "balance", "balance": bank_response["data"] })
    else:
        return create_bad_request_response()

def handle_request_get_owner_name(request_obj, bank):
    if "account" in request_obj:
        account = request_obj["account"]
        bank_response = bank.get_owner_name(account)
        if(bank_response["status"] != ERROR_TYPE.NO_ERROR):
            return create_error_response(bank_response)
        else:
            return json.dumps({
                "type": "account_info", 
                "name": bank_response["data"]["name"],
                "account": bank_response["data"]["account"]
            })
    else:
        return create_bad_request_response()

def handle_request_remove_account(request_obj, bank):
    if all (key in request_obj for key in ("account_to_remove", "account", "token")):
        account_to_remove = request_obj["account_to_remove"]
        account            = request_obj["account"         ]
        token              = request_obj["token"           ]
        bank_response = bank.remove_account(account_to_remove, account, token)
        return handle_default_response(bank_response)
    else:
        return create_bad_request_response()

def create_error_response(bank_response):
    error_bank_response = bank_response["status"]
    if error_bank_response == ERROR_TYPE.NON_SUFFICIENT_FUNDS:
        return json.dumps({ "type": "non_sufficient_funds", "error_message": ""})
    elif error_bank_response  == ERROR_TYPE.INVALID_ACCOUNT:
        return json.dumps({ "type": "invalid_account", "error_message": ""})
    elif error_bank_response == ERROR_TYPE.INVALID_DESTINATION_ACCOUNT:
        return json.dumps({ "type": "invalid_account", "error_message": ""})
    elif error_bank_response  == ERROR_TYPE.INVALID_TOKEN:
        return json.dumps({ "type": "invalid_token", "error_message": ""})
    elif error_bank_response  == ERROR_TYPE.WRONG_PASSWORD:
        return json.dumps({ "type": "wrong_password", "error_message": ""})
    elif error_bank_response == ERROR_TYPE.NOT_A_MANAGER:
        return json.dumps({ "type": "not_a_manager", "error_message": ""})
    elif error_bank_response == ERROR_TYPE.INVALID_AMOUNT:
        return json.dumps({ "type": "invalid_amount", "error_message": "Amount can't be negative." })
    # This should never happen
    else:
        Logger.log_error("Fatal: Bank response is unknown.")
        return json.dumps({ "type": "bad_request", "error_message": ""})

def create_ok_response(message = ""):
    return json.dumps({ "type": "ok", "message": message})

def create_bad_request_response(message = ""):
    return json.dumps({ "type": "bad_request", "message": message })

def handle_default_response(bank_response):
    if bank_response["status"] != ERROR_TYPE.NO_ERROR:
        return create_error_response(bank_response)
    else:
        return create_ok_response()

def assert_types(request_obj):
    EXPECTED_TYPES = {
        "op":                   str,
        "id":                   str,
        "name":                 str,
        "account":              str,
        "destination_account":  str,
        "password":             str,
        "token":                str,
        "account_to_remove":    str,
        "is_manager":           bool
    }
    # Amount needs special verification because it can either be
    # int or float
    for key in request_obj:
        value = request_obj[key]
        if key == "amount":
            if not isinstance(value, int) and not isinstance(value, float):
                return False
            # Amount should never be negative
            elif value < 0:
                return False
        elif not isinstance(value, EXPECTED_TYPES[key]):
            return False
    return True