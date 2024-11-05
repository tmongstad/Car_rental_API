from project.model.order_management import generate_order, cancel_order, get_order_by_customer
from flask import request, jsonify
from project import app
from project.model import messages
from project.model.car_management import get_car, update_car

@app.route('/order_car', methods = ['POST'])
def order_car():
    # Gets the needed data
    user_data = request.get_json()
    car_id = user_data['car_id']
    customer_id = user_data['customer_id']
    if not car_id or not customer_id:
        return messages.missing_field_error('car id or customer id')
    # Checks the input
    try: 
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        messages.int_error('customer_id and car_id')
    # Checks if a customer already has placed an order.
    customer_booked = get_order_by_customer(customer_id)
    if customer_booked:
        return jsonify({
            'Message': 'Customer already has placed an order',
            'Status': 'Unable',
            'Data': customer_booked
        })
    # Checks if the car is unavailable.
    car = get_car(car_id)
    if car['status'] == 'unavailable':
        return jsonify({
            'Message': 'Car is unavailable',
            'Status': 'unavailable',
            'Data': car
        })
    # Checks if the car is available
    if car['status'] == 'available':
        update_car(car_id, {'status': 'available'})
        order_data = generate_order(customer_id, car_id)
        return messages.success('Order', 'Order ID', order_data[0]['order']['order_id'], order_data)
    else:
        return jsonify('Something went wrong') # If something else should happen.
    
@app.route('/cancel_order_car', methods = ['DELETE'])
def cancel_order_car():
    data = request.get_json()
    car_id, customer_id = data['car_id'], data['customer_id']
    if not car_id or not customer_id:
        return messages.missing_field_error('car id or customer id')
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('car_id and customer_id')
    order_data = cancel_order(car_id, customer_id)
    return messages.check_results('Order', 'Connected to', f'car: {car_id} and customer: {customer_id}', order_data, 'canceled')

