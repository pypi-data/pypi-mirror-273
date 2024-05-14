import socket
import inspect

class Request:
    def __init__(self, method, path, headers, body, client_address):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.client_address = client_address

class Response:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def encode(self):
        return f"HTTP/1.1 {self.status_code} OK\r\n".encode() + \
               "\r\n".join(f"{k}: {v}" for k, v in self.headers.items()).encode() + \
               b"\r\n\r\n" + self.body

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        self.routes[path] = handler

    def get_route(self, path):
        return self.routes.get(path)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.router = Router()
        self.before_request_funcs = []

    def start(self):
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

        body = None

        if lines[-1]:
            body = lines[-1].decode('utf-8')

        return Request(method, path, headers, body, client_address)

    def find_handler(self, request_path):
        handler = self.router.get_route(request_path)
        if handler is None:
            return self.default_handler, {}
        return handler, {}

    def handle_request(self, request):
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
        response.status_code = 404
        response.body = b"Not Found"

    def default_response(self, response):
        response.status_code = 500
        response.body = b"Internal Server Error"

    def route(self, path):
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    def send_html(self, file_path):
        with open(file_path, "r") as f:
            html_content = f.read()
        return Response(200, {'Content-Type': 'text/html'}, html_content.encode())

    def before_request(self, func):
        self.before_request_funcs.append(func)
        return func
