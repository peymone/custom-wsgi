import socket
from sys import argv
from configparser import ConfigParser
from select import select

from wsgi_client import Client


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port

        # Create a server socket and enable listen mod
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()

        tasks.append(self.accept_connection())

        print(f"Server started on http://{self.__host}:{self.__port}")

    def accept_connection(self):
        """Accept connections and start request handling for clients"""

        while True:
            yield ('read', self.__sock)
            client_sock, client_addr = self.__sock.accept()
            tasks.append(self.handle_connection(client_sock))

    def handle_connection(self, client_socket: socket.socket):
        yield ('read', client_socket)
        request = client_socket.recv(1024)
        print(request)

        if request:
            wsgi_client.create_connection()
            wsgi_client.send(request)
            headers, body = wsgi_client.recieve()

            yield ('write', client_socket)
            client_socket.sendall(headers)
            client_socket.sendall(body)


def load_config(config_file: str) -> tuple[str, int, str, int]:
    """Load server settings from a config file"""

    config = ConfigParser()
    config.read(config_file)
    server_host = config['SERVER']['Host']
    server_port = config['SERVER']['Port']
    wsgi_host = config['WSGI']['Host']
    wsgi_port = config['WSGI']['Port']

    return server_host, int(server_port), wsgi_host, int(wsgi_port)


def event_loop():
    rdict, wdict = dict(), dict()

    while any([tasks, rdict, wdict]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(rdict, wdict, [])

            for sock in ready_to_read:
                tasks.append(rdict.pop(sock))
            for sock in ready_to_write:
                tasks.append(wdict.pop(sock))

        try:
            task = tasks.pop(0)  # Get first generator
            reason, sock = next(task)  # Iterate to the next yield

            match reason:
                case 'read': rdict[sock] = task
                case 'write': wdict[sock] = task

        except StopIteration:
            pass


if __name__ == '__main__':
    tasks = list()

    host, port, wsgi_host, wsgi_port = load_config('config.ini')
    proxy = Server(host, port)
    wsgi_client = Client(wsgi_host, wsgi_port)

    event_loop()
