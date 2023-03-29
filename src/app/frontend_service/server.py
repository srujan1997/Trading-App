from http.server import ThreadingHTTPServer
from request_handler import request_handler


class updatedHTTPServer(ThreadingHTTPServer):
    protocol_version = 'HTTP/1.1'
    max_threads = 2

#host = input("Enter hostname: ")
host_name = '0.0.0.0'
httpd = updatedHTTPServer((host_name, 8081), request_handler.FrontEndHandler)
print(f'Serving on port 8081...')
httpd.serve_forever()
