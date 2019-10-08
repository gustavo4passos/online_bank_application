import json
from bank   import ERROR_TYPE
from logger import Logger

def handle_request(request, bank):
    request_obj = json.loads(request)

    if("op" not in request_obj):
        return create_bad_request_response("Request is missing operation specifier.")

    if request_obj['op'] == 's':
        return handle_request_withdraw(request_obj, bank)
    elif request_obj['op'] == 'l':
        return handle_request_login(request_obj, bank)
    else:
        response = { "type": "bad_request" }
        return json.dumps(response)

def handle_request_withdraw(request_obj, bank):
    if "account" in request_obj and "amount" in request_obj and "token" in request_obj:
        account = request_obj["account"]
        amount  = request_obj["amount"]
        token   = request_obj["token"]
        bank_response = bank.withdraw(account, amount, token)

        #This should never happen
        if "status" not in bank_response:
            Logger.log_error("Fatal: Bank response has no status field")
            return create_bad_request_response()
        if(bank_response["status"] != ERROR_TYPE.NO_ERROR):
            return create_error_response(bank_response)            
        else:
            return create_ok_response()
    else:
        return create_bad_request_response()

def handle_request_login(request_obj, bank):
    if "account" in request_obj and "password" in request_obj:
        account  = request_obj["account" ]
        password = request_obj["password"]
        bank_response = bank.login(account, password)

        #This should never happen
        if "status" not in bank_response:
            Logger.log_error("Fatal: Bank response has no status field")
            return create_bad_request_response()
        
        if(bank_response["status"] != ERROR_TYPE.NO_ERROR):
            return create_error_response(bank_response)
        else:
            name    = bank_response["data"]["name"   ]
            token   = bank_response["data"]["token"  ]
            balance = bank_response["data"]["balance"]
            return json.dumps({ 
                "type": "login_success", 
                "name": name, 
                "balance": balance, 
                "token": token
            })
    else:
        return create_bad_request_response()
    

def create_error_response(bank_response):
    if bank_response["status"] == ERROR_TYPE.NON_SUFFICIENT_FUNDS:
        return json.dumps({ "type": "non_sufficient_funds", "error_message": ""})
    elif bank_response["status"] == ERROR_TYPE.INVALID_ACCOUNT:
        return json.dumps({ "type": "invalid_account", "error_message": ""})
    elif bank_response["status"] == ERROR_TYPE.INVALID_TOKEN:
        return json.dumps({ "type": "invalid_token", "error_message": ""})
    elif bank_response["status"] == ERROR_TYPE.WRONG_PASSWORD:
        return json.dumps({ "type": "wrong_password", "error_message": ""})
    # This should never happen
    else:
        Logger.log_error("Fatal: Bank response is unknown.")
        return json.dumps({ "type": "bad_request", "error_message": ""})

def create_ok_response(message = ""):
    return json.dumps({ "type": "ok", "message": message})

def create_bad_request_response(message = ""):
    return json.dumps({ "type": "bad_request", "message": message })