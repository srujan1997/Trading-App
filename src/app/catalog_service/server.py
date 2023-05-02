from concurrent import futures
import grpc
import os

from models.models import load_catalog
from request_handler.request_handler import CatalogHandlerServicer
from request_handler.catalog_handler_pb2_grpc import add_CatalogHandlerServicer_to_server


# Main server method
def serve():
    load_catalog()
    host_name = os.environ.get("HOST_IP", "localhost")
    port = '5297'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    add_CatalogHandlerServicer_to_server(CatalogHandlerServicer(), server)
    server.add_insecure_port(host_name + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
