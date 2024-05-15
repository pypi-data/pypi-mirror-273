import socket
import inspect
import json
from time import time
import http

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
        status_line = f"HTTP/1.1 {self.status_code} {http.HTTPStatus(self.status_code).phrase}\r\n"
        headers_lines = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        return (status_line + headers_lines + "\r\n\r\n").encode() + self.body
    
class Router:
    """Handles routing of HTTP requests to appropriate handlers."""
    def __init__(self):
        """Initialize a Router object."""
        self.routes = {}
        self.rate_limits = {}

    def add_route(self, path, handler, methods=None, rate_limit=None, rate_limit_expire=None):
        """
        Add a route to the router.

        Parameters:
        - path (str): The route path.
        - handler (callable): The handler function for the route.
        - methods (list): List of HTTP methods supported by this route (e.g., ['GET', 'POST']).
        - rate_limit (int): The rate limit per IP address (requests per unit time).
        - rate_limit_expire (int): The duration in seconds for which the rate limit should be enforced.
        """
        self.routes[path] = {'handler': handler, 'methods': methods}
        if rate_limit:
            self.rate_limits[path] = {'limit': rate_limit, 'expire': rate_limit_expire, 'requests': []}

    def get_route(self, path):
        """
        Get the handler for the specified route path.

        Parameters:
        - path (str): The route path.

        Returns:
        - callable: The handler function for the route, or None if not found.
        """
        return self.routes.get(path)

    def check_rate_limit(self, path, client_ip):
        """
        Check if the client IP has exceeded the rate limit for the specified path.

        Parameters:
        - path (str): The route path.
        - client_ip (str): The client's IP address.

        Returns:
        - bool: True if the rate limit is exceeded, False otherwise.
        """
        if path in self.rate_limits:
            limit_info = self.rate_limits[path]
            limit = limit_info['limit']
            expire = limit_info.get('expire')
            requests = limit_info['requests']

            now = time()
            requests[:] = [timestamp for timestamp in requests if now - timestamp <= expire]

            if len(requests) >= limit:
                return True
            else:
                requests.append(now)
        return False

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
        self.error_handlers = {}

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

        if len(lines) < 1:
            raise ValueError("Malformed request: Start line is missing")
        start_line = lines[0].decode('utf-8')
        start_line_parts = start_line.split(' ')
        if len(start_line_parts) != 3:
            raise ValueError("Malformed request: Start line does not contain expected elements")
        method, path, version = start_line_parts

        headers = {}
        body = None

        for line in lines[1:]:
            if not line:
                break
            if b':' in line:
                header_parts = line.split(b': ', 1)
                if len(header_parts) != 2:
                    raise ValueError("Malformed request: Header line does not contain expected elements")
                header, value = header_parts
                headers[header.decode('utf-8')] = value.decode('utf-8')
            else:
                pass

        client_ip = headers.get('X-Forwarded-For', '').split(',')[0].strip() or client_address[0]

        if b'\r\n\r\n' in request_data:
            body_start = request_data.index(b'\r\n\r\n') + len(b'\r\n\r\n')
            body = request_data[body_start:]

        return Request(method, path, headers, body, (client_ip, client_address[1]))

    def find_handler(self, request_path, request_method):
        """
        Find the appropriate handler for the given request path and method.

        Parameters:
        - request_path (str): The request path.
        - request_method (str): The HTTP method.

        Returns:
        - tuple: A tuple containing the handler function and any additional kwargs.
        """
        route = self.router.get_route(request_path)
        if route:
            handler = route.get('handler')
            methods = route.get('methods', [])
            if handler and (not methods or request_method in methods):
                return handler, {}
            else:
                return self.method_not_allowed, {}
        else:
            return self.default_handler, {}

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

        handler, kwargs = self.find_handler(request_path=request.path, request_method=request.method)

        if handler:
            if self.router.check_rate_limit(request.path, request.client_address[0]):
                return Response(429, {}, b"Rate Limit Exceeded")
            
            if inspect.signature(handler).parameters:
                result = handler(request, response, **kwargs)
                if isinstance(result, tuple) and len(result) == 2:
                    status_code, body = result
                    return Response(status_code, {}, body.encode())
                else:
                    return Response(500, {}, b"Internal Server Error")
            else:
                return handler()
        else:
            route = self.router.get_route(request.path)
            if route:
                methods = route.get('methods', [])
                if methods and request.method not in methods:
                    return Response(405, {}, b"Method Not Allowed")
            self.default_response(response)

        return response

        return response

    def default_handler(self, request, response):
        """Default request handler for 404 Not Found."""
        response.status_code = 404
        response.body = b"Not Found"

    def method_not_allowed(self, request, response):
        """Request handler for 405 Method Not Allowed."""
        response.status_code = 405
        response.body = b"Method Not Allowed"

    def default_response(self, response):
        """Default response handler for 500 Internal Server Error."""
        response.status_code = 500
        response.body = b"Internal Server Error"

    def route(self, path, methods=None, rate_limit=None, rate_limit_expire=None):
        """
        Decorator for defining routes.

        Parameters:
        - path (str): The route path.
        - methods (list): List of HTTP methods supported by this route (e.g., ['GET', 'POST']).
        - rate_limit (int): The rate limit per IP address for this route.
        - rate_limit_expire (int): The duration in seconds for which the rate limit should be enforced.

        Returns:
        - callable: The decorator function.
        """
        def decorator(func):
            self.router.add_route(path, func, methods=methods, rate_limit=rate_limit, rate_limit_expire=rate_limit_expire)
            return func
        return decorator

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