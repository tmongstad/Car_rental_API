from project.model.query_management import run_query
from project.model import messages
from flask import request

def get_all_customers():
    query = "MATCH (customer:Customer) RETURN customer"
    data = run_query(query)
    return data # Returns a list of all customers [{'customer':{'customer_1': 1}}, {'customer':{'customer_2': 1}}...]

def add_customer(name, age, address):
    # Creates a query:
    query = """
    CREATE (customer:Customer {name: $name, age:$age, address:$address})
    SET customer.customer_id = id(customer) 
    RETURN customer
    """
    customer_data = run_query(query, {'name':name, 'age':age, 'address':address}) # Runs the query, with the parameters provided
    if customer_data:
        return customer_data[0]['customer']  # as a dict{'customer_id': customer_id, 'name':name, 'age':age, 'address':address}
    else:
        return []

def get_customer(customer_id):
    query = "MATCH (customer:Customer {customer_id:$customer_id}) RETURN customer"
    customer_data = run_query(query, {'customer_id':customer_id})
    if customer_data:
        return customer_data[0]['customer'] # {'customer_id': customer_id, 'name':name, 'age':age, 'address':address}
    else:
        return []

def update_customer(fields, customer_id):
    query_variable = ','.join([f'customer.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (customer:Customer{{customer_id:$customer_id}})
    SET {query_variable}
    RETURN customer
    """
    customer_data = run_query(query, {'customer_id':customer_id, **fields})
    if customer_data:
        return customer_data[0]['customer'] # {'customer_id': customer_id, 'name':name, 'age':age, 'address':address}
    else:
        return []

def delete_customer(customer_id):
    customer_data = get_customer(customer_id)
    if customer_data:
        query = "MATCH (customer:Customer {customer_id:$customer_id}) DETACH DELETE customer RETURN COUNT(customer) AS deleted_count"
        result = run_query(query, {'customer_id':customer_id})
        if result[0]['deleted_count'] == 1:
            return {'deleted_customer': customer_data}
        else:
            return [] # If query fails
    else:
        return [] # If 
