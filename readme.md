# Simple Online Bank Simulator
A simple online bank simulator using a client-server architecture written in Python.

## Usage
To run the application you need Python 3 installed. To check if it is installed in your computer run python3 --version from the terminal.
To install Python 3 on Ubuntu (or other Linux distributions that apt is available), run sudo apt install python3

### Running the server
The server is located inside the 'server' folder. To start it, run 'python3 server.py`. The default port is 7049. It needs to be running before trying to connect from a client.

### Running the client
The CLI client is located inside the client folder. It can be started by running 'python3 client_cli.py'

### Protocol
A description of the request and response messages are located inside the protocol folder