from http.server import BaseHTTPRequestHandler
import json
import grpc
import csv
from threading import Lock
import threading

from request_handler import catalog_handler_pb2
from request_handler import catalog_handler_pb2_grpc
from request_handler import order_handler_pb2
from request_handler import order_handler_pb2_grpc

txn_id = 0
lock = Lock()

class FrontEndHandler(BaseHTTPRequestHandler):

    # Helper function to process the order
    def run_order(self,stock_name, volume, trade_type):
        global txn_id, lock
        hostname = 'localhost'
        port = '5298'
        with grpc.insecure_channel(hostname+':'+port) as channel:
            stub = order_handler_pb2_grpc.OrderHandlerStub(channel)
            response = stub.Order(order_handler_pb2.Request(stock_name=stock_name,trade_volume=volume, type=trade_type))
        if response.success == 1:
            lock.acquire()
            log_file = open("transaction_log.csv", "a", encoding='UTF8', newline='')
            data = [txn_id, stock_name, trade_type, volume]
            writer = csv.writer(log_file)
            writer.writerow(data)
            log_file.close()
            txn_id += 1
            lock.release()
            return response.success, txn_id
        else:
            return response.success, -1
    
    #Helper function to run lookup
    def run_lookup(self, stock_name):
        hostname = 'localhost'
        port = '5297'
        with grpc.insecure_channel(hostname+':'+port) as channel:
            stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
            response = stub.Lookup(catalog_handler_pb2.LookupRequest(stock_name=stock_name))
        if response.success == 1:
            return response.stock_details
        else:
            return {}

    #overrriding the GET method
    def do_GET(self):
        stock_name = self.path.split('/')[-1]
        stock = self.run_lookup(stock_name)
        if stock:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": {
                    "name": stock_name,
                    "price": stock['price'],
                    "quantity": stock['quantity']
                }
            }
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "error": {
                    "code": 404,
                    "message": "Stock not found"
                }
            }
        self.wfile.write(json.dumps(response).encode())

    #overrriding the POST method
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        order = json.loads(post_data)
        if order['type']=="sell" or order['type'] =="buy":
            success,txn_id = self.run_order(order['name'], order['quantity'], order['type'])
        else:
            txn_id = -1
        if txn_id==-1:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "error": {
                    "code": 400,
                    "message": "Invalid order request"
                }
            }
        elif txn_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": {
                    "transaction_number": txn_id
                }
            }

        self.wfile.write(json.dumps(response).encode())
