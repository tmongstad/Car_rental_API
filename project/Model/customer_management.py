from project.model.query_management import run_query
from project.model import messages
from flask import request

def add_customer():
    user_data = request.get_json()
    name = user_data['name'] # Gets the make from the posted JSON.
    age = user_data['age']
    address = user_data['address']
    try:
        age = int(age)
    except ValueError:
        return messages.int_error('age')
    if not name or not age or not address:
        return messages.missing_field_error(missing_fields_as_string='name, age and address')
    query = """
    CREATE (customer:Customer {name: $name, age:$age, address:$address})
    SET customer.customer_id = id(customer) 
    RETURN customer
    """
    returned_data = run_query(query, {'name':name, 'age':age, 'address':address}) # Runs the query, with the parameters provided
    return returned_data

def get_all_customers():
    query = "MATCH (customer:Customer) RETURN customer"
    data = run_query(query)
    if data:
        return data
    else:
        return "No data"

def get_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer_id')
    query = "MATCH (customer:Customer {customer_id:$customer_id}) RETURN customer"
    results = run_query(query, {'customer_id':customer_id})
    if results:
        return messages.success('Customer', 'ID', customer_id, results[0], 'recieve')
    else:
        return messages.no_results('Customer', 'customer_id', customer_id)

def update_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer_id')
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
    
    query_variable = ','.join([f'customer.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (customer:Customer{{customer_id:$customer_id}})
    SET {query_variable}
    RETURN customer
    """
    results = run_query(query, {'customer_id':customer_id, **fields})
    if results:
        return messages.success('Customer', 'ID', customer_id, results[0], 'update')
    else:
        return messages.no_results('Customer', 'customer_id', customer_id)

def delete_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer_id')
    query = "MATCH (customer:Customer {customer_id:$customer_id}) DETACH DELETE customer RETURN COUNT(customer) AS deleted_count"
    result = run_query(query, {'customer_id':customer_id})
    return result
