from project.model.car_management import get_car
from project.model.customer_management import get_customer
from project.model.query_management import run_query
from project.model import messages
from flask import request

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


