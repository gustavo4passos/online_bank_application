import json
import threading

from enum   import Enum
from logger import Logger

class ERROR_TYPE(Enum):
	NO_ERROR = 0,
	INVALID_ACCOUNT = 1,
	INVALID_DESTINATION_ACCOUNT = 2,
	INVALID_ID = 3,
	INVALID_MANAGER_ACCOUNT = 4
	NON_SUFFICIENT_FUNDS = 5
	WRONG_PASSWORD = 6

class Bank:
	def __init__(self, database_file):
		self.database_file_name = database_file
		json_db_file = open(database_file)
		self.database = json.load(json_db_file)
		json_db_file.close()

		self.dump_db_lock = threading.Lock()
		self.database_access_lock = threading.Lock()
		Logger.log_info("Bank database has loaded.")
	
	def get_balance(self, account_number):
		if account_number in self.database:
			self.database_access_lock.acquire()
			result = { 
				"status": ERROR_TYPE.NO_ERROR,
				"data": self.database[account_number] }
			self.database_access_lock.release()

			return result

		else:
			return {
				"status": ERROR_TYPE.INVALID_ACCOUNT,
				"data": "" }
	
	def withdraw(self, account_number, amount):
		if account_number in self.database:
			self.database_access_lock.acquire()
			if self.database[account_number]["balance"] < amount:
				self.database_access_lock.release()
				return {
				"status": ERROR_TYPE.NON_SUFFICIENT_FUNDS,
				"data": ""
				}

			self.database[account_number]["balance"] -= amount
			self.update_database()
			self.database_access_lock.release()
			
			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}

		else:
			return {
				"status": ERROR_TYPE.INVALID_ACCOUNT,
				"data": ""
			}

	def deposit(self, destination_account, amount):
		if destination_account in self.database:
			self.database_access_lock.acquire()
			self.database[destination_account]["balance"] += amount
			self.update_database()
			self.database_access_lock.release()

			return { 
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}

		else:
			return {
				"status": ERROR_TYPE.INVALID_ACCOUNT,
				"data": ""
			}	
	
	def transfer(self, origin_account, destination_account, amount):
		if (origin_account in self.database) and (destination_account in self.database):
			self.database_access_lock.acquire()
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

			return {
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}
		else:
			if origin_account in self.database:
				return{
				"status": ERROR_TYPE.INVALID_DESTINATION_ACCOUNT,
				"data": ""
				}
			else:
				return{
				"status": ERROR_TYPE.INVALID_ACCOUNT,
				"data": ""
				}	
	
	def login(self, account, password):
		if account in self.database:
			self.database_access_lock.acquire()
			if self.database[account]["password"] == password:
				self.database_access_lock.release()

				return {
					"status": ERROR_TYPE.NO_ERROR,
					"data": "Accepted login"
				}

			else:
				self.database_access_lock.release()
				return{
					"status": ERROR_TYPE.WRONG_PASSWORD,
					"data": ""
				}

		else:
			return {
					"status": ERROR_TYPE.INVALID_ACCOUNT,
					"data": ""
				}	
	
	def create_account(self, identification, name, password, manager_account):
		self.database_access_lock.acquire()
		if manager_account in self.database and self.database[manager_account]["is_manager"]:
			new_account_number = self.database["private"]["next_account_number"]
			self.database["private"]["next_account_number"] = self.database["private"]["next_account_number"] + 1
			print(new_account_number)
			data = {
				new_account_number:{
					"id":identification,
					"name":name,
					"password":password,
					"balance":0,
					"is_manager":0
				}
			}
			self.database.update(data)
			self.update_database()
			self.database_access_lock.release()
			json_db_file = open(self.database_file_name)
			self.database = json.load(json_db_file)
			json_db_file.close()
			return{
				"status": ERROR_TYPE.NO_ERROR,
				"data": ""
			}
		else:
			self.database_access_lock.release()
			return{
				"status":ERROR_TYPE.INVALID_MANAGER_ACCOUNT,
				"data": ""
			}	
	
	
	def update_database(self):
		# Acquires database file access lock
		self.dump_db_lock.acquire()		

		# Dumps bank database to json file	
		db_file = open(self.database_file_name, "w+")
		json.dump(self.database, db_file)
		db_file.close()

		# Releases database file access lock
		self.dump_db_lock.release()

	def get_database(self):
		return self.database
		

