from configparser import ConfigParser
from select import select
import socket

from wsgi_client import Client


class Server:
    """Proxy server for redirect requests to the WSGI (application) server"""

    def __init__(self, host: str, port: int) -> None:
        """Set proxy host and port, create socket"""

        self.__host = host
        self.__port = port
        self.__balancer = self.__balancer()  # Generator object for balancing

        # Create a server socket and enable listen mod
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()

        # Add client acception method to the task for event loop
        tasks.append(self.accept_connection())

        print(f"Server started on http://{self.__host}:{self.__port}")

    def accept_connection(self):
        """Accept connections and start request handling for clients"""

        while True:
            yield ('read', self.__sock)  # Return socket for event loop and stop here

            # Accept client and add handling method to the task for event loop
            client_sock, client_addr = self.__sock.accept()
            tasks.append(self.handle_connection(client_sock))

    def handle_connection(self, client_socket: socket.socket):
        """Redirect request to the application server and send back ready data to the client"""

        yield ('read', client_socket)  # Return socket for event loop and stop here
        request = client_socket.recv(1024)  # Get data from client

        if request:
            wsgi_server = next(self.__balancer)
            print(wsgi_server)

            wsgi_client.create_connection(wsgi_server)  # Create connection with application server
            wsgi_client.send(request)  # Redirect request to the WSGI (application) server
            headers, body = wsgi_client.recieve()  # Recieve data from application server

            yield ('write', client_socket)  # Return socket for event loop and stop here

            # Send data back to the client
            client_socket.sendall(headers)
            client_socket.sendall(body)

    def __balancer(self):
        """generator for balancing the load on application servers"""

        while True:
            for host, port in wsgi_servers.items():
                yield host, port


def load_config(config_file: str) -> tuple[str, int, dict]:
    """Load server settings from a config file"""

    config = ConfigParser()
    config.read(config_file)
    server_host = config['SERVER']['Host']
    server_port = config['SERVER']['Port']
    wsgi_hosts = config['WSGI']['Host']
    wsgi_ports = config['WSGI']['Port']

    # Application server can be more than one - for balancing purpose
    wsgi_hosts = wsgi_hosts.split()
    wsgi_ports = [int(port) for port in wsgi_ports.split()]

    wsgi_servers = dict()
    for host, port in zip(wsgi_hosts, wsgi_ports):
        wsgi_servers[host] = port

    return server_host, int(server_port), wsgi_servers


def event_loop():
    """Event loop to populate tasks and execute generators code"""

    rdict, wdict = dict(), dict()  # Dicts for sock:generators pairs

    while any([tasks, rdict, wdict]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(rdict, wdict, [])  # Get sock ready for action

            # Fill tasks list for executing
            for sock in ready_to_read:
                tasks.append(rdict.pop(sock))
            for sock in ready_to_write:
                tasks.append(wdict.pop(sock))

        try:
            task = tasks.pop(0)  # Get first generator
            reason, sock = next(task)  # Iterate to the next yield (execute code)

            # Fill dicts for select()
            match reason:
                case 'read': rdict[sock] = task
                case 'write': wdict[sock] = task

        except StopIteration:
            pass


if __name__ == '__main__':
    host, port, wsgi_servers = load_config('config.ini')
    tasks = list()  # Generators for event loop
    proxy = Server(host, port)
    wsgi_client = Client()

    event_loop()
