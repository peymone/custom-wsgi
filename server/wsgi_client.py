import socket


class Client:
    def __init__(self, wsgi_host: str, wsgi_port: int) -> None:
        self.__wsgi_host = wsgi_host
        self.__wsgi_port = wsgi_port

        self.__wsgi = (self.__wsgi_host, self.__wsgi_port)

    def create_connection(self) -> None:
        """Connect to WSGI (applicatioon) server"""

        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__client_sock.connect(self.__wsgi)

    def send(self, data: bytes) -> None:
        self.__client_sock.sendall(data)

    def recieve(self) -> tuple[bytes, bytes]:
        headers = self.__client_sock.recv(1024)
        body = self.__client_sock.recv(1024)
        self.__client_sock.close()

        return headers, body
