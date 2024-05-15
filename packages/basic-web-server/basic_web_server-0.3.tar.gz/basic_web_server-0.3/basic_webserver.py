import socket
import inspect
import json

class Request:
    """Represents an HTTP request."""

    def __init__(self, method, path, headers, body, client_address):
        """
        Initialize a Request object.

        Parameters:
        - method (str): The HTTP method (e.g., 'GET', 'POST').
        - path (str): The request path.
        - headers (dict): The request headers.
        - body (str): The request body.
        - client_address (tuple): The client's address (IP, port).
        """
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.client_address = client_address

class Response:
    """Represents an HTTP response."""

    def __init__(self, status_code, headers, body):
        """
        Initialize a Response object.

        Parameters:
        - status_code (int): The HTTP status code.
        - headers (dict): The response headers.
        - body (bytes): The response body.
        """
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def encode(self):
        """
        Encode the response into bytes for sending over the network.

        Returns:
        - bytes: The encoded response.
        """
        status_line = f"HTTP/1.1 {self.status_code} OK\r\n"
        headers_lines = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        return (status_line + headers_lines + "\r\n\r\n").encode() + self.body

class Router:
    """Handles routing of HTTP requests to appropriate handlers."""

    def __init__(self):
        """Initialize a Router object."""
        self.routes = {}

    def add_route(self, path, handler):
        """
        Add a route to the router.

        Parameters:
        - path (str): The route path.
        - handler (callable): The handler function for the route.
        """
        self.routes[path] = handler

    def get_route(self, path):
        """
        Get the handler for the specified route path.

        Parameters:
        - path (str): The route path.

        Returns:
        - callable: The handler function for the route, or None if not found.
        """
        return self.routes.get(path)

class Server:
    """Represents an HTTP server."""

    def __init__(self, host: str=None, port: int=None, config_file: str=None):
        """
        Initialize a Server object.

        Parameters:
        - host (str): The host IP address.
        - port (int): The port number.
        - config_file (str): The path to a configuration file.
        """
        if config_file:
            self.load_config_from_file(config_file)
        else:
            if host is None or port is None:
                raise ValueError("Both host and port must be provided if no config file is specified.")
            self.host = host
            self.port = port

        self.router = Router()
        self.before_request_funcs = []

    def load_config_from_file(self, config_file):
        """
        Load server configuration from a file.

        Parameters:
        - config_file (str): The path to the configuration file.
        """
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.host = config.get('host')
        self.port = config.get('port')

        if self.host is None or self.port is None:
            raise ValueError("Invalid configuration file. Host and port must be specified.")

    def start(self):
        """Start the HTTP server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        print("\033[92mApp has successfully started.\n")
        print("\033[91mNote: This application is in early alpha will have bugs, this is not meant for a production environment.\033[0m")

        try:
            while True:
                client_socket, address = self.socket.accept()
                try:
                    request_data = client_socket.recv(1024)
                    request = self.parse_request(request_data, address)
                    response = self.handle_request(request)
                    client_socket.sendall(response.encode())
                except Exception as e:
                    print(f"Error handling request: {e}")
                finally:
                    client_socket.close()
        except KeyboardInterrupt:
            print("\033[91mServer stopped.\033[0m")
        finally:
            if self.socket:
                self.socket.close()

    def parse_request(self, request_data, client_address):
        """
        Parse an HTTP request.

        Parameters:
        - request_data (bytes): The raw request data.
        - client_address (tuple): The client's address (IP, port).

        Returns:
        - Request: The parsed request object.
        """
        lines = request_data.split(b'\r\n')
        start_line = lines[0].decode('utf-8')
        method, path, version = start_line.split(' ')
        headers = {}

        for line in lines[1:]:
            if b':' in line:
                header, value = line.decode('utf-8').split(': ', 1)
                headers[header] = value
            else:
                pass

        client_ip = headers.get('X-Forwarded-For', '').split(',')[0].strip() or client_address[0]

        body = None

        if lines[-1]:
            body = lines[-1].decode('utf-8')

        return Request(method, path, headers, body, (client_ip, client_address[1]))

    def find_handler(self, request_path):
        """
        Find the appropriate handler for the given request path.

        Parameters:
        - request_path (str): The request path.

        Returns:
        - tuple: A tuple containing the handler function and any additional kwargs.
        """
        handler = self.router.get_route(request_path)
        if handler is None:
            return self.default_handler, {}
        return handler, {}

    def handle_request(self, request):
        """
        Handle an incoming HTTP request.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """
        response = Response(200, {}, b"")

        for func in self.before_request_funcs:
            func(request)

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.signature(handler).parameters:
                result = handler(request, response, **kwargs)
                if isinstance(result, Response):
                    return result
                elif isinstance(result, str):
                    return Response(200, {'Content-Type': 'text/html'}, result.encode())
                elif isinstance(result, tuple) and len(result) == 2:
                    status_code, body = result
                    return Response(status_code, {}, body.encode())
                else:
                    return Response(500, {}, b"Internal Server Error")
            else:
                return handler()
        else:
            self.default_response(response)

        return response

    def default_handler(self, request, response):
        """Default request handler for 404 Not Found."""
        response.status_code = 404
        response.body = b"Not Found"

    def default_response(self, response):
        """Default response handler for 500 Internal Server Error."""
        response.status_code = 500
        response.body = b"Internal Server Error"

    def route(self, path):
        """
        Decorator for defining routes.

        Parameters:
        - path (str): The route path.

        Returns:
        - callable: The decorator function.
        """
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    def send_html(self, file_path):
        """
        Send an HTML file as a response.

        Parameters:
        - file_path (str): The path to the HTML file.

        Returns:
        - Response: The HTTP response object.
        """
        with open(file_path, "r") as f:
            html_content = f.read()
        return Response(200, {'Content-Type': 'text/html'}, html_content.encode())

    def before_request(self, func):
        """
        Register a function to be called before handling each request.

        Parameters:
        - func (callable): The function to be called.

        Returns:
        - callable: The registered function.
        """
        self.before_request_funcs.append(func)
        return func
