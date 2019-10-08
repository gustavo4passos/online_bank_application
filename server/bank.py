import json
import threading

from enum   import Enum
from logger import Logger

class ERROR_TYPE(Enum):
	NO_ERROR                    = 0,
	INVALID_ACCOUNT             = 1,
	INVALID_DESTINATION_ACCOUNT = 2,
	INVALID_ID                  = 3,
	NOT_A_MANAGER               = 4,
	NON_SUFFICIENT_FUNDS        = 5,
	WRONG_PASSWORD              = 6,
	INVALID_TOKEN               = 7,
	INVALID_AMOUNT    			= 8

class Bank:
	def __init__(self, database_file):
		self.database_file_name = database_file
		json_db_file = open(database_file)
		self.database = json.load(json_db_file)
		json_db_file.close()

		self.invalid_token_response   = { "status": ERROR_TYPE.INVALID_TOKEN,   "data": "" }
		self.invalid_amount_response  = { "status": ERROR_TYPE.INVALID_AMOUNT,  "data": "" }
		self.invalid_account_response = { "status": ERROR_TYPE.INVALID_ACCOUNT, "data": "" }
		self.dump_db_lock = threading.Lock()
		self.database_access_lock = threading.Lock()
		Logger.log_info("Bank database has loaded.")
	
	def get_balance(self, account_number, token):
		if not self.validate_token(account_number, token):
			return self.invalid_token_response

		self.database_access_lock.acquire()
		if account_number not in self.database:
			self.database_access_lock.release()
			return self.invalid_account_response

		else:
			result = { 
				"status": ERROR_TYPE.NO_ERROR,
				"data": self.database[account_number]["balance"] 
			}
			self.database_access_lock.release()
			return result
	
	def withdraw(self, account_number, amount, token):
		if not self.validate_token(account_number, token):
			return self.invalid_token_response

		if amount < 0:
			return self.invalid_amount_response

		self.database_access_lock.acquire()
		if account_number in self.database:
			if self.database[account_number]["balance"] < amount:
				self.database_access_lock.release()
				return {
					"status": ERROR_TYPE.NON_SUFFICIENT_FUNDS,
					"data": ""
				}

			self.database[account_number]["balance"] -= amount
			self.update_database()
			self.database_access_lock.release()
			
			Logger.log_info("Withdraw operation on account: " + account_number)
			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}

		else:
			self.database_access_lock.release()
			return self.invalid_account_response

	def deposit(self, destination_account, amount):
		if amount < 0:
			return self.invalid_amount_response

		self.database_access_lock.acquire()
		if destination_account in self.database:
			self.database[destination_account]["balance"] += amount
			self.update_database()
			self.database_access_lock.release()

			Logger.log_info("Deposit operation on account: " + destination_account)
			return { 
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}

		else:
			self.database_access_lock.release()
			return self.invalid_account_response
	
	def transfer(self, origin_account, destination_account, amount, token):
		if not self.validate_token(origin_account, token):
			return self.invalid_token_response

		if amount < 0:
			return self.invalid_amount_response
	
		self.database_access_lock.acquire()
		if origin_account in self.database and destination_account in self.database:
			if self.database[origin_account]["balance"] < amount:
				self.database_access_lock.release()
				return {
					"status": ERROR_TYPE.NON_SUFFICIENT_FUNDS,
					"data": ""
				}

			self.database[origin_account]["balance"] -= amount	
			self.database[destination_account]["balance"] += amount
			self.update_database()
			self.database_access_lock.release()

			Logger.log_info("Transfer operation from account '" + origin_account + "' to account '" + destination_account + "'")
			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}
		else:
			self.database_access_lock.release()
			if origin_account in self.database:
				return{
				"status": ERROR_TYPE.INVALID_DESTINATION_ACCOUNT,
				"data": ""
				}
			else:
				self.database_access_lock.release()
				return self.invalid_account_response
	
	def login(self, account, password):
		self.database_access_lock.acquire()
		if account in self.database:
			if self.database[account]["password"] == password:
				self.database_access_lock.release()

				return {
					"status": ERROR_TYPE.NO_ERROR,
					"data": {
						"token": password,
						"name": self.database[account]["name"],
						"balance": self.database[account]["balance"],
					}
				}

			else:
				self.database_access_lock.release()
				return{
					"status": ERROR_TYPE.WRONG_PASSWORD,
					"data": ""
				}

		else:
			self.database_access_lock.release()
			return self.invalid_account_response
	
	def create_account(self, identification, name, password, manager_account, is_manager, token):
		if not self.validate_token(manager_account, token):
			return self.invalid_token_response

		self.database_access_lock.acquire()
		if manager_account not in self.database:
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.INVALID_ACCOUNT,
				"data": ""
			}		
		elif not self.database[manager_account]["is_manager"]:
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.NOT_A_MANAGER,
				"data": ""
			}
		else:
			new_account_number = self.database["private"]["next_account_number"]
			self.database["private"]["next_account_number"] += 1

			self.database[str(new_account_number)] = {
					"id": identification,
					"name": name,
					"password": password,
					"balance": 0,
					"is_manager": is_manager
			}

			self.update_database()
			self.database_access_lock.release()
			Logger.log_info("New account created. Number: " + str(new_account_number))

			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}
	
	def remove_account(self, account_to_remove, manager_account, token):
		if not self.validate_token(manager_account, token):
			return self.invalid_token_response

		self.database_access_lock.acquire()
		if manager_account not in self.database:
			self.database_access_lock.release()
			return self.invalid_account_response

		elif not self.database[manager_account]["is_manager"]:
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.NOT_A_MANAGER,
				"data": ""
			}

		elif account_to_remove not in self.database:
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.INVALID_DESTINATION_ACCOUNT,
				"data": ""
			}
		else:
			del self.database[account_to_remove]
			self.update_database()
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}

	def get_owner_name(self, account):
		self.database_access_lock.acquire()
		if account not in self.database:
			self.database_access_lock.release()
			return self.invalid_account_response

		else:
			self.database_access_lock.release()
			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": {
					"name": self.database[account]["name"],
					"account": account
				}
			}

	def update_database(self):
		# Acquires database file access lock
		self.dump_db_lock.acquire()		

		# Dumps bank database to json file	
		db_file = open(self.database_file_name, "w+")
		json.dump(self.database, db_file, indent=4)
		db_file.close()

		# Releases database file access lock
		self.dump_db_lock.release()

	def validate_token(self, account, token):
		self.database_access_lock.acquire()
		if account not in self.database:
			self.database_access_lock.release()
			return False
		if self.database[account]["password"] != token:
			self.database_access_lock.release()
			return False

		self.database_access_lock.release()
		return True