### Instructions to run

Before entering any of the service directories, please do install all the required libraries by running
pip3 install -r requirements.txt

### Running Locally/edlab

1. Under each directory of services, you would need to execute python3 server.py to start up services.
2. Once done, you can run the client.py file and appropriately mention the inputs for it.
3. Or just manually hit or execute the GET and POST requests from Postman or browser to evaluate the services.

### Using client.py

1. The client.py file resides in the frontend_service directory.
2. On execution, it will ask the user to pass hostname, number of requests and the trade request probability

###  Using docker-compose:

1. docker network create lab - Create this network initially
2. docker-compose build && docker-compose up -d - To start services.
3. docker-compose down - To stop the application.

### Performance Evaluation

1. Please go to the frontend_service directory and execute the file performance.py to get average latency results for trade and lookup.
2. If you instead want to execute multiple clients concurrently, please run load_test.sh in the frontend_service directory. Currently, it can run for 6 clients concurrently, but you can edit it and run for as many clients as you want.

To execute the load_test.sh file, follow the below steps:

1. chmod u+x load_test.sh
2. ./load_test.sh

### Running Test Cases

1. To run test cases, please go to app/tests and run the pytest command to generate the output of testcases. Please ensure all the servers are up and running for it.

### Contributor Notes:

Please find the performance evaluation report for part 3, design documents, output files and test cases output in the docs directory.

A brief division of work between the team members:

Srujan(srujan1997) : Development of order_service, catalog_service, application containeriztion, and design doc
Tejas(tejasgnaik) : Development of frontend_service, performance evaluation, generating output files, writing testcases and design doc

Note: We have utilised 1 free days for this lab.

Late Days Used for Lab1: 2
Late Days Used for Lab2: 1
Total Late Days Used: 3