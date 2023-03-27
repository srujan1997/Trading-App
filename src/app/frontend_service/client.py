import requests
import random
import time

def run_client(percentage):
    session = requests.Session()
    for i in range(5):
        # Lookup a random stock
        stock_name = random.choice(["GameStart", "FishCo", "BoarCo","MenhirCo"])
        response = session.get(f'http://localhost:8081/stocks/{stock_name}')
        if response.status_code == 404:
            print(f"Error: {response.json()['error']['message']}")
        else:
            data = response.json()['data']
            print(f"Stock: {data['name']} - Price: {data['price']} - Quantity: {data['quantity']}")
            # Place a trade request with a certain probability
            if data['quantity'] > 0 and random.random() < percentage:
                quantity = random.randint(1, min(10, data['quantity']))
                response = session.post('http://localhost:8081/orders', json={
                    'name': stock_name,
                    'quantity': quantity,
                    'type': 'sell'
                })
                if response.status_code == 404:
                    print(f"Error: {response.json()['error']['message']}")
                else:
                    data = response.json()['data']
                    print(f"Order placed successfully. Transaction number: {data['transaction_number']}")
        time.sleep(3)

if __name__ == '__main__':
    run_client(0.6)


