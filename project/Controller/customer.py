from project.model.customer_management import get_all_customers, add_customer, get_customer, update_customer, delete_customer
from flask import request
from project import app
from project.model import messages


@app.route('/customer', methods = ['GET', 'POST'])
def manage_customer():
    # Gets all customers:
    if request.method == 'GET':
        data = get_all_customers()
        return messages.check_results('All customers', 'none', 'none', data, 'found')
    
    # Adds a customer:
    if request.method == 'POST':
        user_data = request.get_json()
        name = user_data['name'] # Gets the make from the posted JSON.
        age = user_data['age']
        address = user_data['address']
        try:  # Checks the input
            age = int(age)
        except ValueError:
            return messages.int_error('age')
        if not name or not age or not address:
            return messages.missing_field_error(missing_fields_as_string='name, age and address')
        data = add_customer(name, age, address)
        return messages.check_results('Customer', 'customer ID', data['customer_id'], data, 'added')

# Route for getting, updating and deleting specific car-data
@app.route('/customer/<customer_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_customers(customer_id):
    # Validate the input
    try:
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer_id')
    
    # Gets a specific customer:
    if request.method == 'GET':
        customer_data = get_customer(customer_id)
        return messages.check_results('Customer', 'customer ID', customer_id, customer_data, 'recieve')

    # Updates a customer:
    if request.method == 'PUT':
        data = request.get_json()
        fields = {}
        if 'name' in data:
            fields['name'] = data['name']
        if 'age' in data:
            try:
                data['age'] = int(data['age'])
            except ValueError:
                return messages.int_error('age')
            fields['age'] = data['age']
        if 'address' in data:
            fields['address'] = data['address']
        customer_data = update_customer(fields, customer_id)
        return messages.check_results('Customer', 'ID', customer_id, customer_data, 'update')

    # Deletes a customer by 
    if request.method == 'DELETE':
        data = delete_customer(customer_id)
        return messages.check_results('Customer', 'customer ID', customer_id, data, 'delete')