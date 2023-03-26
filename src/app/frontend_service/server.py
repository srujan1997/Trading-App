from concurrent import futures
import grpc

# Main server method
def serve():
    host_name = "localhost"
    port = '8081'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    server.add_insecure_port(host_name + ':' + port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
