from concurrent import futures
import grpc

from models.models import load_catalog
from request_handler.request_handler import RequestHandlerServicer
from request_handler.catalog_handler_pb2_grpc import add_RequestHandlerServicer_to_server

#Main server method
def serve():
    load_catalog()
    host_name = "localhost"
    port = '5297'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_RequestHandlerServicer_to_server(RequestHandlerServicer(), server)
    server.add_insecure_port(host_name + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
