import grpc
import random
from request_handler import order_handler_pb2
from request_handler import order_handler_pb2_grpc


# Running trade command for when requested by client
def run_trade(stock_name, volume, trade_type):
    # hostname = "0.0.0.0"
    # port = str(6297)
    with grpc.insecure_channel("0.0.0.0:6297")as channel:
        stub = order_handler_pb2_grpc.OrderHandlerStub(channel)
        response = stub.Order(order_handler_pb2.Request(stock_name=stock_name,
                                                        trade_volume=int(volume), type=trade_type))
    print("Trade client received: " + str(response.success)+"  -  "+str(response.transaction_id))


# The main client method
def client(requests):
    stock_names = ["GameStart", "FishCo", "BoarCo", "MenhirCo", "Meta"]
    for i in range(requests):
        stock_name = random.choices(stock_names, weights=[23, 23, 23, 23, 8])
        volume = random.randint(-10, 100)
        trade_type = random.choice(["buy", "sell"])
        run_trade(stock_name[0], volume, trade_type)
        data = [stock_name[0], volume, trade_type]
        print(f"Lookup client requested: {data}")


if __name__ == '__main__':
    no_of_requests = int(input("No of requests:"))  # Mention the number of requests
    client(no_of_requests)
