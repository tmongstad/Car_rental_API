from project.model.car_management import get_car, update_car
from project.model.customer_management import get_customer
from project.model.query_management import run_query
from project.model import messages
from flask import request, jsonify

def generate_order(car_id, customer_id):
    car_data = get_car(car_id)
    customer_order_history = get_order_details(customer_id)
    car_status = car_data['status']
    if car_status == 'unavailable':
        return 'unavailable'
    if customer_order_history:
        return 'booked'
    else:
        query = """
        MATCH (c:Customer {customer_id: $customer_id}), (car:Car {car_id: $car_id})
        CREATE (c)-[:PLACED]->(o:Order)-[:FOR]->(car)
        SET o.order_id = id(o)
        RETURN o"""
        order_data = run_query(query, {'customer_id':customer_id, 'car_id':car_id})
        return order_data

def cancel_order(car_id, customer_id):
    order_data = get_order_details(customer_id)
    if order_data:
        change_booking_status(car_id, 'available')
        delete_order(order_data['order_id'])
    else:
        return None

def delete_order(order_id):
    query = """
    MATCH (o:Order {order_id: $order_id})
    DETACH DELETE o
    RETURN COUNT(o) AS deleted_count
    """
    result = run_query(query, {'order_id': order_id})
    return result

def get_order_details(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        messages.int_error('customer id')    
    query = query = """
    MATCH (c:Customer {customer_id: $customer_id})-[r:PLACED]->(o:Order)-[:FOR]->(car:Car)
    RETURN c AS customer, o AS order, car AS car
    """
    order_data = run_query(query, {'customer_id':customer_id})
    return order_data


def change_booking_status(car_id, status = 'available'):
    return update_car(car_id, {'status': status})

