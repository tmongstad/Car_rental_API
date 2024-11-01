from project.model.customer_management import get_all_customers, add_customer, get_customer, update_customer, delete_customer
from flask import jsonify, request
from project import app


@app.route('/customer', methods = ['GET', 'POST'])
def manage_customer():
    if request.method == 'GET':
        return get_all_customers()
    if request.method == 'POST':
        return add_customer()

# Route for getting, updating and deleting specific car-data
@app.route('/customer/<customer_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_cars(customer_id):
    if request.method == 'GET':
        return get_customer(customer_id)
    if request.method == 'PUT':
        return update_customer(customer_id)
    if request.method == 'DELETE':
        return delete_customer(customer_id)