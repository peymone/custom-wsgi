import socket  # just for understanding, use wsgiref instead
import importlib.util
from threading import Thread
from configparser import ConfigParser


class WSGIgateway:
    """Application server for interacting with a web server by WSGI standard"""

    def __init__(self, host: str, port: int, wsgi_app) -> None:
        """""Set application server host and port, create socket"""

        self.__host = host
        self.__port = port
        self.__wsgi_app = wsgi_app

        # Create a server socket and enable listen mod
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen()

        print(f"WSGI Server started on http://{self.__host}:{self.__port}")

    def accept_conenction(self) -> None:
        """Accept connections and start request handling for clients"""

        while True:
            client_socket, client_address = self.__socket.accept()
            client_thread = Thread(target=self.handle_connection, args=(client_socket, ), daemon=True)
            client_thread.start()

    def handle_connection(self, client_socket: socket.socket) -> None:
        request = client_socket.recv(1024).decode()
        request = request.split()

        # Request parsing - in actual application server like gunicorn parsed every parameters
        environ = dict()
        environ['PATH_INFO'] = request[1]
        environ['REQUEST_METHOD'] = request[0]
        environ['SERVER_PROTOCOL'] = request[2]

        # Call this from WSGI application
        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            """Send response status and headers to the client"""

            response_headers = "\r\n".join([f"{header}: {value}" for header, value in headers])
            response = f"HTTP/1.1 {status}\r\n{response_headers}\r\n\r\n"
            client_socket.sendall(response.encode())

        # Call the WSGI application and send response body to the client
        response_body = self.__wsgi_app(environ, start_response)
        for data in response_body:
            client_socket.sendall(data.encode())

        # Close connection after sending data
        client_socket.close()


def load_config(config_file: str) -> tuple[str, str, int]:
    """Load wsgi and server settings from a config file"""

    config = ConfigParser()
    config.read(config_file)
    module_path = config['WSGI']['ModulePath']
    application_name = config['WSGI']['ApplicationName']
    server_host = config['SERVER']['Host']
    server_port = config['SERVER']['Port']

    return module_path, application_name, server_host, int(server_port)


def load_application(module_path: str, application_name: str):
    """Import WSGI application function from an external module"""

    spec = importlib.util.spec_from_file_location(application_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, application_name)


if __name__ == '__main__':
    # Configurate application server
    module_path, application_name, server_host, server_port = load_config('config.ini')
    wsgi_application = load_application(module_path, application_name)
    wsgi_gateway = WSGIgateway(server_host, server_port, wsgi_application)

    # Start application server
    wsgi_gateway.accept_conenction()
