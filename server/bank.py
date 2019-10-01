import json
import threading
from enum import Enum

class ERROR_TYPE(Enum):
	NO_ERROR = 0,
	INVALID_ACCOUNT = 1,
	INVALID_DESTINATION_ACCOUNT = 2,
	INVALID_ID = 3,
	NOT_A_MANAGER = 4

class Bank:
	def __init__(self, database_file):
		self.database_file_name = database_file
		json_db_file = open(database_file)
		self.database = json.load(json_db_file)
		json_db_file.close()

		self.dump_db_lock = threading.Lock()
		self.database_access_lock = threading.Lock()
		print("Bank database has loaded")
	
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
				"data": "" 
				}
	
	def withdraw(self, account_number, amount):
		if account_number in self.database:
			self.database_access_lock.acquire()
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

	def deposit(self, destination_acount, amount):
		return
	
	def transfer(self, origin_account, destination_account, amount):
		return
	
	def login(self, account, password):
		return
	
	def create_acount(self, id, name, manager_account):
		return
	
	def update_database(self):
		# Acquires database file access lock
		self.dump_db_lock.acquire()		

		# Dumps bank database to json file	
		db_file = open(self.database_file_name, "w+")
		json.dump(self.database, db_file)
		db_file.close()

		# Releases database file access lock
		self.dump_db_lock.release()
