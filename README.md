# Trading Application Backend (Asterix and Double Trouble)

   `✅` Distributed Application with microservices architecture <br>
   `✅` Highly Consistent <br>
   `✅` Scalable <br>
   `✅` Fault Tolerant <br>
   `✅` Concurrent Request Handling <br>
   `✅` Replication <br>
   `✅` Cache <br>
   `✅` Containerized <br>
   `✅` Deploy on AWS <br>
   `✅` Performance Testing <br>

[Design Document] (https://github.com/srujan1997/Trading_App/blob/main/docs/design_document.pdf)

## Description

Backend for a stock trading platform.The application consists of three microservices: 
a front-end service, a catalog service, and an order service. To ensure high performance and tolerance 
to failures, modern design practices were used. Implemented a two-tier design (a front-end tier and a
back-end tier)  for the app using microservices at each tier. The front-end is implemented as a single 
microservice, while the back-end is implemented as two separate services: a stock catalog service and 
an order service.

### Front-end Service

The clients can communicate with the front-end service using REST APIs. The client can look up the details 
of available stocks, place order and query placed orders. The server listens to HTTP requests on a socket port 
and assigns them to a thread pool. A simple thread-per-request model is used. The thread parses the HTTP request 
to extract the GET/POST command and redirects request to the Catalog or Order service as mentioned below. 
The response from this back-end service is used to construct a json response and sent back to the client as response.

### Catalog Service

The  catalog service maintains a list of all stocks traded in the stock market. It maintains the trading volume 
of each stock and the number of stocks available for sale. When the front-end service receives a Lookup request, 
it will forward the request to the catalog service. The catalog service maintains the catalog data, both in 
memory and in a CSV or text file on disk ("database"). The disk file will persist the state of the catalog. 
When the service starts up, it initializes itself from the database disk file.

While lookup requests simply read the catalog, trade requests will be sent to the order service, which will 
then contact the catalog service to update  the volume of stocks traded in the catalog. It will also increment 
or decrement the number of stocks available for sale, depending on the type of trade request. Stocks of each 
company available for sale are initialized to 100.

The catalog service is implemented as a server that listens to request from the front-end service or the order 
service. The catalog service exposes an internal gRPC interface to these two components.

Like the front-end server, threads are employed to service incoming request. Since the catalog can be accessed 
concurrently by more than one thread, synchronization is used to protect reads and updates to the catalog. 
Read-write locks were used for higher performance.

### Order Service

When the front-end service receives an order request, it will forward the request to the order service. 
The order service still interacts with the catalog service to complete the order. Specifically, a buy trade 
request succeeds only if the remaining quantity of the stock is greater than the requested quantity, and the 
quantity is decremented. A sell trade request simply increase the remaining quantity of the stock.

If the order was successful, the order service generates an transaction number and returns it to the 
front-end service. The order service also maintains the order log (including transaction number, stock name,
order type, and quantity) in a persistent manner. Similar to the catalog service, a simple CSV or text file 
on disk is used as the persistent storage (database). The catalog service exposes an internal gRPC interface

Like in the catalog service, threads are used. Further, the order service is threaded and uses synchronization 
when writing to the order database file. 


### Client

The client opens a HTTP connection with the front-end service and randomly looks up a stock. If the returned 
quantity is greater than zero, with probability $p$ it will send another order request using the same 
connection. $p$ is adjustable parameter in the range $[0, 1]$ to test application performance when the 
percentage of order requests changes. A client can make a sequence of lookup and trade for each such lookup 
based on probability $p$. The front-end server uses a single thread to handle all requests from the session 
until the client closes the HTTP socket connection.

The client first queries the front-end service with a random stock, then it will make a follow-up trade request 
with probability `p` (make `p` an adjustable variable). You can decide whether the stock query request and the 
trade request use the same connection. The client will repeat the aforementioned steps for a number of iterations, 
and record the order number and order information if a trade request was successful. Before exiting, the client 
will retrieve the order information of each order that was made using the order query request, and check whether 
the server reply matches the locally stored order information.

### Caching

Redis is used as cache in the front-end service to reduce the latency of the stock lookup requests. The 
front-end server starts with an empty in-memory cache. Upon receiving a stock query request, it first 
checks the in-memory cache or forwards it to the catalog service, and then cache the returned result by 
the catalog service.

Cache consistency is addressed whenever a stock is bought or sold using server-push technique: 
the catalog server sends invalidation requests to the front-end server after each trade. 
The invalidation requests cause the front-end service to remove the corresponding stock from the cache.

### Replication

To ensure fault tolerance of order information due to crash failures, the order service is replicated. A simple 
leader election algorithm was designed to ensure consistency. There is always 1 leader and the rest are
followers. When the stock bazaar application is built, first the catalog service starts. Then three 
replicas of the order service each with a unique id start and they have their own database files.
The front-end service will always pick the node with the highest id as the leader.

When the front-end service starts, it will read the id number and address of each replica of the 
order service. It will ping the replica with the highest id number to see if it's responsive. 
If so it will notify all the replicas that a leader with a specific id has been selected, otherwise 
it will try the replica with the second-highest id. The process repeats until a leader has been found.

When a trade request or an order query request arrives, the front-end service only forwards the request to 
the leader. In case of a successful trade, the leader node will propagate the information of the new order 
to the follower nodes to maintain data consistency.

### Fault Tolerance

Crash failure tolerance is ensured rather than Byzantine failure tolerance.

When any replica crashes (including the leader), trade requests and order query requests can still 
be handled. To achieve this, if the front-end service finds that the leader node is unresponsive, it 
will redo the leader selection algorithm as described in [Replication](#replication).

When a crashed replica is back online, it synchronizes with the other replicas to retrieve the order 
information that it has missed during the crash time. When a replica comes back online from a crash, it 
will look at its database file and get the latest order number that it has and ask the other replicas what 
orders it has missed since that order number.

## Deployment

All components are containerized and deployed as a distributed application using Docker.

## Instructions to run

Install all the required libraries by running
`pip3 install -r requirements.txt`

### Run Locally

1. Create network - `docker network create lab`
2. Start services - `docker-compose build && docker-compose up -d `
3. USE `curl` or postman (see design document for sample requests) to interact with Front-end service.
4. Stop application - `docker-compose down`

### Performance Evaluation

1. Go to the frontend_service directory and execute the file performance.py to get average latency results 
   for trade and lookup.
2. If you want to execute multiple clients concurrently, run load_test.sh in the frontend_service directory. 
   Currently, it runs for 5 clients concurrently, but it can be edited and run for as many clients as necessary.

To execute the load_test.sh file, follow the below steps:
`chmod u+x load_test.sh`
`./load_test.sh`

### Run Test Cases

To run test cases, go to app/tests and run the `pytest` command to generate the output of testcases. 
Ensure all the servers are up and running for it.

## Results - Testing and Evaluation with Deployment on AWS and Local

Deployed the application on an `m5a.xlarge` instance in the `us-east-1` region on AWS for testing.

Run 5 clients on your local machine or AWS and measured the latency seen by each client for different types 
of requests. Change the probability p of a follow-up trade request from 0 to 80%, with an increment of 20%, 
and record the result for each p setting. The same experiments can be done with cache turned off to estimate 
the benefits of cache.

Finally, crash failures can be simulated by killing a random order service replica while the client is running, 
and then bring it back online after some time. Repeat this experiment several times and try to test the case 
when the leader is killed.

[Performance Testing Results] (https://github.com/srujan1997/Trading_App/blob/main/docs/performance_testing_results.pdf)<br>
[Sample Outputs] (https://github.com/srujan1997/Trading_App/blob/main/docs/output_snippets.pdf)<br>

### Contributors
[Srujan] (https://github.com/srujan1997/)<br>
[Tejas] (https://github.com/tejasgnaik/)<br>

## References

1. Learn about Gaul (the region) https://en.wikipedia.org/wiki/Gaul and the Gauls (the people) https://en.wikipedia.org/wiki/Gauls<br>
2. Learn about the comics that this project is based on https://en.wikipedia.org/wiki/Asterix
