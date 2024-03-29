# Online Bank Application
A simple online bank application using a client-server architecture written in Python. It supports simple operations such as withdrawal, deposit, transfer and checking account balances. Accounts with manager permissions can also create and remove accounts. The bank database is stored on disk on the server side, and is therefore persistent. It was created for learning purposes, and it's a simple example on client-server architecture.

## Usage
The application needs Python 3 installed. To check if it is installed in your system run 'python3 --version' from the terminal.
To install Python 3 on Ubuntu (or other Linux distributions where apt is available), run 'sudo apt install python3'

### Running the server
The server is located inside the 'server' folder. To start it, run 'python3 server.py'. The default port is 7049.

### Running the client
The CLI client is located inside the client folder. It can be started by running 'python3 client_cli.py'

### Protocol
A description of the request and response messages are located inside the protocol folder
