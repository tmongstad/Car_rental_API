# Car Rental API

## Overview
This is the car rental API by Sami and Torstein, as a 

plaintext
Kopier kode
This is a car rental management system built with Flask, Neo4j, and Python. It manages cars, customers, orders, and employees, providing endpoints for creating, updating, and deleting resources.

Table of Contents
Getting Started
Prerequisites
Installation
Configuration
Running the Application
Usage

## Endpoints

### Car endpoints:

#### Get all cars, add car
@app.route('/cars', methods = ['GET', 'POST'])
def manage_cars():
GET: return all cars
POST: Adds a car 
    requests data in json-format: {"make":make, "model":model, "year":year, "location": location, "status":status}
    return car_data in json-format {"car_id":car_id, "make":make, "model":model, "year":year, "location": location, "status":status}

#### getting, updating and deleting  by car_id
    @app.route('/cars/<car_id>', methods = ['GET', 'PUT', 'DELETE'])
    def handle_cars(car_id):
        GET: returns car by car_id
        PUT: updates car by car_id
            requests data in json-format: {"make":make, "model":model, "year":year, "location": location, "status":status}
            returns the updated car data
        DELETE: deletes a car by car_id.
            returns the deleted car

### Customer endpoints:

#### Get all customers, add customer:
    @app.route('/customer', methods = ['GET', 'POST'])
    def manage_customer():
        GET: Return all customers
        POST: Adds a customer
            Requests data in json-format {'name':name, 'age':age, 'address':address}
            Returns data in json-format {'customer_id': customer_id, 'name':name, 'age':age, 'address':address}

#### Getting, updating and deleting customer by customer_id:
    @app.route('/customer/<customer_id>', methods = ['GET', 'PUT', 'DELETE'])
    def handle_customers(customer_id):
        GET: returns customer by customer_id {"customer_id":customer_id, "name":name, "age":age, "address":address}
        PUT: updates customer by customer_id
            requests data in json-format: {"name":name, "age":age, "address":address}
            returns the updated customer data {"customer_id":customer_id, "name":name, "age":age, "address":address}
        DELETE: deletes a customer by employee_id.

### Employee endpoints:

#### Get all cemployee, add employee:
    @app.route('/employee', methods = ['GET', 'POST'])
    def manage_employee():
        GET: Return all employees
        POST: Adds a employee
            Requests data in json-format {'name':name, 'branch':branch, 'address':address}
            Returns data in json-format {'employee_id': employee_id, 'name':name, 'branch':branch, 'address':address}

#### Getting, updating and deleting employee by employee_id:
    @app.route('/employee/<employee_id>', methods = ['GET', 'PUT', 'DELETE'])
    def handle_customers(employee_id):
        GET: returns employee by employee_id {"employee_id":employee_id, "name":name, "age":age, "address":address}
        PUT: updates employee by employee_id
            requests data in json-format: {'name':name, 'branch':branch, 'address':address}
            returns the updated employee data {"employee_id":employee_id, 'name':name, 'branch':branch, 'address':address}
        DELETE: deletes a employee by employee_id.

### Order Endpoints:

#### Endpoint: Get all orders:
    @app.route('/get_orders', methods = ['GET'])
    def all_orders():
    GET: Return all orders and customer and cars connected to it:
##### example of returned data:
[
    {
        "car": {
            "car_id": 1,
            "loc": "Bergen",
            "make": "VW",
            "model": "Golf",
            "status": "booked",
            "year": 1986
        },
        "customer": {
            "address": "Germany",
            "age": 180,
            "customer_id": 24,
            "name": "Albert Einstein"
        },
        "order": {
            "order_id": 42
        }
    },
    {
        ...Next order...
    }
]

#### Endpoint: Order car
    @app.route('/order_car', methods = ['POST'])
    def order_car():
        POST - Creates a order in database, a relation between customer and car, and changes status of car to 'booked'
            requests car_id and customer_id in jsonformat {'car_id':car_id, 'customer_id':customer_id}
            returns - customer data of the customer who placed the order, the order itself and the car.
    {
        "car": {
            "car_id": 1,
            "loc": "Bergen",
            "make": "VW",
            "model": "Golf",
            "status": "booked",
            "year": 1986
        },
        "customer": {
            "address": "Germany",
            "age": 180,
            "customer_id": 24,
            "name": "Albert Einstein"
        },
        "order": {
            "order_id": 42
        }
    }

#### Endpoint: Rent car: 
    @app.route('/rent_car', methods = ['PUT'])
    def rent_car():
        Updates the car status to 'Rented'
        requests - car_id and customer_id
        returns the rented car.

#### Endpoint: Return car:
    @app.route('/return_car', methods = ['PUT'])
    def return_car(): 
        requests car_id, customer_id and status of car (either 'ok' or 'damaged')
        Updates the car status to 'available' if car is not damaged, and deletes the order. If damaged, new status 'damaged'

#### Endpoint: Cancel order:
    @app.route('/cancel_order_car', methods = ['DELETE'])
    def cancel_order_car():
        requests car_id and customer_id
        Cancels the order - sets status of car to 'available' and deletes the order and connections between car and customer

#### Endpoint: Fix car:
    @app.route('/fix_car', methods=['PUT'])
    def fix_car():
        requests car_id and changes status of car to available.

## Testing
    Link to Postman via API: pm for request

## Prerequisites
List the software and tools required for running the project.
- **Python 3.x**
- **Neo4j Database** (local or cloud-based)
- **Flask** web framework
- **Postman** for API testing (optional, for testing purposes)

## Git clone:
    https://github.com/tmongstad/Car_rental_API.git

