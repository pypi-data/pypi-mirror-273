import socket
import threading
from typing import Union


class Client:
    def __init__(self, host: str, port: Union[str, int], handler=None):
        """
        Represents client TCP connection. Add handler using @client.add_handler decorator or server.set_handler(handler)
        function.
        """
        self.handler = handler
        self.host = host
        self.port = port
        self.address = str(self.host) + ':' + str(self.port)

        def client():
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = self._socket
            try:
                s.connect((self.host, self.port))
                addr = s.getpeername()

                data = None
                while True:
                    if self.handler is not None:
                        self.handler(addr, s, data)

                    try:
                        data = s.recv(1024)
                    except OSError:
                        data = b''

                    if not data:
                        break
            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError, ConnectionError):
                pass

        self._socket_thread = threading.Thread(target=client)
        self._socket_thread.start()

    def set_handler(self, function):
        """
        Sets a handler for TCP client. Handler format:

        def client_handler(addr: tuple, conn: socket.socket, data: bytes): pass
        """
        self.handler = function
