import socket
import threading
from typing import Union

screen_lock = threading.Semaphore(value=1)


class Server:
    def __init__(self, host: str, port: Union[str, int], handler=None):
        """
        Represents server TCP connection. Add handler using @server.add_handler decorator or server.set_handler(handler)
        function.
        """
        self.handler = handler
        self.host = host
        self.port = port
        self.address = str(self.host) + ':' + str(self.port)
        self.is_listening = False

        def conn_handler(addr, conn: socket.socket):
            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                    except OSError:
                        data = b''

                    if not data:
                        break

                    if self.handler is not None:
                        self.handler(addr, conn, data)

                screen_lock.acquire()
                print(f'Disconnected by {":".join(map(str, addr))}')
                screen_lock.release()

        def server():
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = self._socket
            s.bind((self.host, self.port))
            s.listen()
            screen_lock.acquire()
            print(f'Listening to {":".join(map(str, s.getsockname()))}')
            screen_lock.release()
            self.is_listening = True
            while True:
                try:
                    conn, addr = s.accept()
                    screen_lock.acquire()
                    print(f'Connected by {":".join(map(str, addr))}')
                    screen_lock.release()
                    conn_thread = threading.Thread(target=conn_handler, args=(addr, conn))
                    conn_thread.start()
                except OSError:
                    break

        self._socket_thread = threading.Thread(target=server, daemon=True)
        self._socket_thread.start()

    def set_handler(self, function):
        """
        Sets a handler for TCP server. Handler format:

        def server_handler(addr: tuple, conn: socket.socket, data: bytes): pass
        """
        self.handler = function

    def mainloop(self):
        """Use it to make server stoppable only by KeyboardInterrupt exception."""
        try:
            while not self.is_listening:
                pass
            screen_lock.acquire()
            print('Press Ctrl + C to stop server!')
            screen_lock.release()
            while True:
                pass
        except KeyboardInterrupt:
            if hasattr(self, '_socket'):
                screen_lock.acquire()
                print('Stopping server...')
                screen_lock.release()
                self._socket: socket.socket
                self._socket.close()
