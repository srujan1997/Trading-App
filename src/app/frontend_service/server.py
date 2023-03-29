from http.server import ThreadingHTTPServer
from request_handler import request_handler
import os


class updatedHTTPServer(ThreadingHTTPServer):
    protocol_version = 'HTTP/1.1'
    max_threads = 2

#host = input("Enter hostname: ")
host_name = os.environ.get("HOST_IP", "localhost")
port = 8081
httpd = updatedHTTPServer((host_name, port), request_handler.FrontEndHandler)
print(f'Serving on port 8081...')
httpd.serve_forever()
