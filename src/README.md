### Instructions to run

Before entering any of the service directories, please do install all the required libraries by running
pip3 install -r requirements.txt

### Running Locally using docker-compose

1. docker network create lab - Create this network initially
2. docker-compose build && docker-compose up -d - To start services.
3. Manually hit or execute the GET and POST requests from Postman or browser to evaluate the services.
4. docker-compose down - To stop the application.

### Performance Evaluation on AWS

1. Please go to the frontend_service directory and execute the file performance.py to get average latency results for trade and lookup.
2. If you instead want to execute multiple clients concurrently, please run load_test.sh in the frontend_service directory. Currently, it can run for 5 clients concurrently, but you can edit it and run for as many clients as you want.

To execute the load_test.sh file, follow the below steps:

1. chmod u+x load_test.sh
2. ./load_test.sh

### Database Syncing

In order to ensure fault tolerance, our system is designed to function seamlessly even if one replica experiences an outage. However, it is imperative to always maintain at least one original copy of the data to retrieve the system's state. Without this original copy, the retrieval of the state would be rendered impossible.

### Running Test Cases

1. To run test cases, please go to app/tests and run the pytest command to generate the output of testcases. Please ensure all the servers are up and running for it.

### Contributor Notes:

Please find the performance evaluation report, design documents and output files in the docs directory.

A brief division of work between the team members:

Srujan(srujan1997) : Refactoring code to use Flask framework, replication, leader election and design doc<br>
Tejas(tejasgnaik) : implementing new GET order request, performing performance evaluation, generating output files, deploying into AWS and design doc
