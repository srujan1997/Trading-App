import grpc
import random
from request_handler import catalog_handler_pb2
from request_handler import catalog_handler_pb2_grpc


# Running lookup command for when requested by client
def run_lookup(stock_name):
    hostname = "0.0.0.0"
    port = '5297'
    with grpc.insecure_channel(hostname+':'+port) as channel:
        stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
        response = stub.Lookup(catalog_handler_pb2.LookupRequest(stock_name=stock_name))
    print("Lookup client received: " + str(response.stock_details))


# The main client method
def client(requests):
    stock_names = ["GameStart", "FishCo", "BoarCo", "MenhirCo", "Meta"]
    for i in range(requests):
        stock_name = random.choices(stock_names, weights=[23, 23, 23, 23, 8])
        print("Lookup client requested: " + stock_name[0])
        run_lookup(stock_name[0])


if __name__ == '__main__':
    no_of_requests = int(input("No of requests:"))  # Mention the number of requests
    client(no_of_requests)
