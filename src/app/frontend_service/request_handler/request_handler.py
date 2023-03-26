from http.server import BaseHTTPRequestHandler
import json
import grpc
import csv

from request_handler import order_handler_pb2
from request_handler import order_handler_pb2_grpc
from request_handler import catalog_handler_pb2
from request_handler import catalog_handler_pb2_grpc

class FrontEndHandler(BaseHTTPRequestHandler):

    # Helper function to process the order
    def process_order(stock_name, volume, trade_type):
        global txn_id, lock
        hostname = 'localhost'
        port = '5297'
        with grpc.insecure_channel(hostname+':'+port) as channel:
            stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
            response = stub.Trade(catalog_handler_pb2.TradeRequest(stock_name=stock_name,trade_volume=volume, type=trade_type))
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
    def run_lookup(stock_name):
        hostname = 'localhost'
        port = '5297'
        with grpc.insecure_channel(hostname+':'+port) as channel:
            stub = catalog_handler_pb2_grpc.CatalogHandlerStub(channel)
            response = stub.Lookup(catalog_handler_pb2.LookupRequest(stock_name=stock_name))
        if response.success == 1:
            return response.stock_details
        else:
            return {}

    
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
            self.send_error(404, 'Stock not found')
            response = {
                "error": {
                    "code": 404,
                    "message": "Stock not found"
                }
            }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        order = json.loads(post_data)
        success,txn_id = self.process_order(order['name'], order['quantity'], order['type'])
        if txn_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": {
                    "transaction_number": txn_id
                }
            }
        else:
            self.send_error(400, 'Invalid order request')
            response = {
                "error": {
                    "code": 400,
                    "message": "Invalid order request"
                }
            }
        self.wfile.write(json.dumps(response).encode())
