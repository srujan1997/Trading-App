import requests
import random
import time

# main client method to start client
def run_client(p,num_req,hostname):
    s = requests.Session()
    for i in range(num_req):
        # Run a random for lookup of stocks
        stock_name = random.choice(["GameStart", "FishCo", "BoarCo","MenhirCo"])
        response = s.get(f'http://{hostname}:8081/stocks/{stock_name}')
        if response.status_code == 404:
            print(f"Error: {response.json()['error']['message']}")
        else:
            data = response.json()['data']
            print(f"Lookup for Stock {data['name']}  Price: {data['price']}  Quantity: {data['quantity']}")
            # Placing order request if probability is more
            if data['quantity'] > 0 and p > random.random():
                quantity = 10
                trade_type=random.choice(["sell","buy"])
                response = s.post(f'http://{hostname}:8081/orders', json={
                    'name': stock_name,
                    'quantity': quantity,
                    'type': trade_type
                })
                if response.status_code == 404:
                    print(f"Error: {response.json()['error']['message']}")
                else:
                    order_data = response.json()['data']
                    print(f"Order Request for Stock {data['name']} Transaction number: {order_data['transaction_number']}")
        time.sleep(5)

if __name__ == '__main__':
    hostname = input("Enter hostname: ") #Configure hostname according to the machine
    num_req = int(input("Enter number of requests: "))
    prob = float(input("Set the probability for running trade requests: "))
    run_client(prob,num_req,hostname)


