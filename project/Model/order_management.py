from project.model.car_management import get_car, update_car
from project.model.customer_management import get_customer
from project.model.query_management import run_query
from project.model import messages


def get_all_orders():
    query = """
    MATCH (customer:Customer)-[r:PLACED]->(order:Order)-[:FOR]->(car:Car)
    RETURN customer, order, car
    """
    order_data = run_query(query)
    return order_data

def generate_order(customer_id, car_id): 
    query = """
        MATCH (customer:Customer {customer_id: $customer_id}), (car:Car {car_id: $car_id})
        CREATE (customer)-[:PLACED]->(order:Order)-[:FOR]->(car)
        SET order.order_id = id(order)
        RETURN order, customer, car"""
    order_data = run_query(query, {'customer_id':customer_id, 'car_id':car_id})
    return order_data # Returns [{"order":{}}, {"customer": {}}, {"car": {}}]

def cancel_order(car_id, customer_id):
    order_data = get_order_by_customer(customer_id)
    if order_data:
        change_booking_status(car_id, 'available')
        return delete_order(order_data[0]['order']['order_id'])
    else:
        return None

def returned_car(car_id, customer_id):
    order_data = get_order_by_customer(customer_id)
    if order_data:
        change_booking_status(car_id, 'available')
        return delete_order(order_data[0]['order']['order_id'])
    else:
        return None

def delete_order(order_id):
    query = """
    MATCH (o:Order {order_id: $order_id})
    DETACH DELETE o
    RETURN COUNT(o) AS deleted_count
    """
    result = run_query(query, {'order_id': order_id})
    if result:
        return {'deleted_order': order_id}
    else:
        return None

def get_order_by_customer(customer_id): # Checks if customer already has a order placed
    try:
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer id')    
    query = query = """
    MATCH (c:Customer {customer_id: $customer_id})-[r:PLACED]->(o:Order)-[:FOR]->(car:Car)
    RETURN c AS customer, o AS order, car AS car
    """
    order_data = run_query(query, {'customer_id':customer_id})
    return order_data # Returns [{customer: {}}, {order: {}}, {car: {}}]


def change_booking_status(car_id, new_status):
    return update_car(car_id, {'status': new_status})

