import socket


class Client:
    """Client for redirect requests from proxy server to the application server"""

    def create_connection(self, wsgi_server: tuple[str, int]) -> None:
        """Connect to WSGI (applicatioon) server"""

        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__client_sock.connect(wsgi_server)

    def send(self, data: bytes) -> None:
        """Send request to the application server"""

        self.__client_sock.sendall(data)

    def recieve(self) -> tuple[bytes, bytes]:
        """Recieve data from application server"""

        headers = self.__client_sock.recv(1024)
        body = self.__client_sock.recv(1024)
        self.__client_sock.close()

        return headers, body
