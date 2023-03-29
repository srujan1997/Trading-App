import requests
import random
import time

def performance(p,num_req,hostname):
    s = requests.Session()
    lookup_latency = []
    trade_latency = []
    for i in range(num_req):
        # Run a random for lookup of stocks
        st_lookup = time.time()
        stock_name = random.choice(["GameStart", "FishCo", "BoarCo","MenhirCo"])
        response = s.get(f'http://{hostname}:8081/stocks/{stock_name}')
        end_lookup = time.time()
        lookup_time = end_lookup - st_lookup
        lookup_latency.append(lookup_time)
        time.sleep(1)
        if response.status_code == 404:
            print(f"Error: {response.json()['error']['message']}")
        else:
            data = response.json()['data']
            # print(f"Lookup for Stock {data['name']}  Price: {data['price']}  Quantity: {data['quantity']}")
            # Place a trade request with a certain probability
            if data['quantity'] > 0 and p > random.random():
                st_trade = time.time()
                quantity = 10
                trade_type=random.choice(["sell","buy"])
                response = s.post(f'http://{hostname}:8081/orders', json={
                    'name': stock_name,
                    'quantity': quantity,
                    'type': trade_type
                })
                end_trade = time.time()
                trade_time = end_trade - st_trade
                trade_latency.append(trade_time)
                # if response.status_code == 404:
                #     print(f"Error: {response.json()['error']['message']}")
                # else:
                #     order_data = response.json()['data']
                #     print(f"Order Request for Stock {data['name']} Transaction number: {order_data['transaction_number']}")
        time.sleep(2)
    print("Average lookup latency: "+ str(sum(lookup_latency)/len(lookup_latency)))
    print("Average trade latency: "+str(sum(trade_latency)/len(trade_latency)))

if __name__ == '__main__':
    #hostname = input("Enter hostname: ")
    performance(1,8,"elnux2.cs.umass.edu")