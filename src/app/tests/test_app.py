import requests
import json


# test case for a non-exisiting stock
def test_for_non_existing_stock():
    stock_name = "Microsoft"
    response=requests.get(f"http://localhost:8081/stocks/{stock_name}")
    assert response.status_code == 404


# test case for an invalid request
def test_for_invalid_order_request():
    url = "http://localhost:8081/orders"
    headers = {'Content-type': 'application/json'}
    invalid_data1 = {"name": "GameStart", "quantity": 10, "type": "invalid"}
    invalid_data2 = {"name": "ABC", "quantity": 10, "type": "buy"}
    response1 = requests.post(url, headers=headers, data=json.dumps(invalid_data1))
    response2 = requests.post(url, headers=headers, data=json.dumps(invalid_data2))
    assert response1.status_code == 400
    assert response2.status_code == 400


# test cases for existing stock
def test_for_existing_stock():
    stock_name = "GameStart"
    response=requests.get(f"http://localhost:8081/stocks/{stock_name}")
    assert response.status_code == 200


# test case for a correct order request
def test_for_correct_order_request():
    url = "http://localhost:8081/orders"
    headers = {'Content-type': 'application/json'}
    data = {"name": "GameStart", "quantity": 10, "type": "buy"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 200

