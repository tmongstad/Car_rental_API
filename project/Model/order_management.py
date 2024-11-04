from project.model.car_management import get_car, update_car
from project.model.customer_management import get_customer
from project.model.query_management import run_query
from project.model import messages
from flask import request, jsonify

def generate_order():
    user_data = request.get_json()
    car_id = user_data['car_id']
    customer_id = user_data['customer_id']
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        messages.int_error('customer_id and car_id')
    car_data = get_car(car_id)
    customer_data = get_customer(customer_id)
    query = """
    MATCH (c:Customer {customer_id: $customer_id}), (car:Car {car_id: $car_id})
    CREATE (c)-[:PLACED]->(o:Order)-[:FOR]->(car)
    SET o.order_id = id(o)
    RETURN o"""
    order_data = run_query(query, {'customer_id':customer_id, 'car_id':car_id})
    # order_details = order_data | car_data | customer_data 
    return order_data# messages.success('Order', 'order_id', order_data['order_id'], order_details)


def delete_order():
    pass

def update_order_status():
    pass

def check_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        messages.int_error('customer id')    
    query = query = """
    MATCH (c:Customer {customer_id: $customer_id})-[r:PLACED]->(o:Order)-[:FOR]->(car:Car)
    RETURN c AS customer, o AS order, car AS car
    """
    data = run_query(query, {'customer_id':customer_id})
    car_data = data[0]["car"]
    order_data = data[0]["order"]
    customer_data = data[0]["customer"]
    if data:
        # return car_id, customer_id, and change status
        change_booking_status(car_data['car_id'], 'unavailable')
    else:
        return None
# 

def change_booking_status(car_id, status = 'available'):
    return update_car(car_id, {'status': status})

def check_booking_status(customer_id = None, order_id = None, car_id = None):
    if not customer_id and not order_id and not car_id:
        return messages.missing_field_error('customer_id, order_id or car_id')
    if customer_id:
        pass
    if order_id:
        pass
    if car_id:
        pass
