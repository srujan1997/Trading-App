from concurrent import futures
import grpc

from request_handler.request_handler import OrderHandlerServicer, get_last_txn_id
from request_handler.order_handler_pb2_grpc import add_OrderHandlerServicer_to_server


# Main server method
def serve(host):
    get_last_txn_id()
    host_name = '0.0.0.0'
    port = '6297'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_OrderHandlerServicer_to_server(OrderHandlerServicer(), server)
    server.add_insecure_port(host + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    host = input("Enter hostname: ")
    serve(host)
