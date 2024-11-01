from project.model.query_management import run_query
from project.model import messages
from flask import request, jsonify

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
        return messages.missing_field_error('name, age and address')
    
    query = """
    CREATE (car:Car {make: $make, model:$model, year:$year, location:$location, status:$status})
    SET car.car_id = id(car) 
    RETURN car
    """
    returned_data = run_query(query, {'make':make, 'model':model, 'year':year, 'location':location, 'status':status}) # Runs the query, with the parameters provided
    


    pass

def get_all_customers():
    query = "MATCH (customer:Customer) RETURN customer"
    data = run_query(query)
    return data

def get_customer(customer_id):
    pass

def update_customer(customer_id):
    pass

def delete_customer(customer_id):
    pass