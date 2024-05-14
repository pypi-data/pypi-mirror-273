A module for easy TCP threaded connection.

Example code:
```py
import socket
from sttcp.client import Client
from sttcp.server import Server


# Creating a TCP threaded server
server = Server('localhost', 63552)

# Setting a server handlers
@server.set_handler
def server_handler(addr: tuple, conn: socket.socket, data: bytes):
    # All this code executes when somebody connects the TCP server
    conn.sendall(data)


# Creating a TCP threaded client
client = Client('localhost', 63552)

# Setting a client handler
@client.set_handler
def client_handler(addr: tuple, conn: socket.socket, data: bytes):
    # All this code executes on connection and on receiving response
    if data is None:
        # data is None when is an initial connection
        conn.sendall('Meow'.encode('utf-8'))
    else:
        # data is not None when client got a response after initial
        #   connection request
        print(f'Recieved "{data.decode("utf-8")}"')
        conn.close()


server.mainloop()

```