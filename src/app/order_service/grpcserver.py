from concurrent import futures
from app_factory import create_app
import grpc
import os

from request_handler.request_handler import OrderHandlerServicer, get_last_txn_id
from request_handler.order_handler_pb2_grpc import add_OrderHandlerServicer_to_server

app = create_app(app_name="frontend_service")


# Main server method
def serve():
    get_last_txn_id()
    host_name = os.environ.get("HOST_IP", "localhost")
    port = '6297'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_OrderHandlerServicer_to_server(OrderHandlerServicer(), server)
    server.add_insecure_port(host_name + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    #host = input("Enter hostname: ")
    serve()
    app.run(host='127.0.0.1', port=app.config['APP_PORT'])

