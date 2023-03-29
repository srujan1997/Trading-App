from concurrent import futures
import grpc

from request_handler.request_handler import OrderHandlerServicer, get_last_txn_id
from request_handler.order_handler_pb2_grpc import add_OrderHandlerServicer_to_server


# Main server method
def serve():
    get_last_txn_id()
    host_name = '0.0.0.0'
    port = '5298'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    add_OrderHandlerServicer_to_server(OrderHandlerServicer(), server)
    server.add_insecure_port(host_name + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    #host = input("Enter hostname: ")
    serve()
