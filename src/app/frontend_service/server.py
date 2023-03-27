from concurrent import futures
from logging import Logger
import grpc
from http.server import ThreadingHTTPServer
from request_handler import request_handler


class updatedHTTPServer(ThreadingHTTPServer):
    protocol_version = 'HTTP/1.1'
    max_threads = 5

httpd = updatedHTTPServer(('localhost', 8081), request_handler.FrontEndHandler)
print(f'Serving on port 8081...')
httpd.serve_forever()
