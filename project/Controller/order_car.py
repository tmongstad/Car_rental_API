from project.model.order_management import generate_order, cancel_order
from flask import request, jsonify
from project import app
from project.model import messages


@app.route('/order_car', methods = ['POST'])
def order_car():
    user_data = request.get_json()
    car_id = user_data['car_id']
    customer_id = user_data['customer_id']
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        messages.int_error('customer_id and car_id')
    order = generate_order(car_id, customer_id)
    if order == 'unavailable':
        return 'The car is unavailable'
    elif order == 'booked':
        return 'The customer alredy has a order'
    else:
        return order

@app.route('/cancel_order_car', methods = ['PUT'])
def cancel_order_car():
    data = request.get_json()
    car_id, customer_id = data['car_id'], data['customer_id']
    if not car_id or not customer_id:
        return messages.missing_field_error('car id or customer id')
    try:
        car_id, customer_id = int(car_id), int(customer_id)
    except ValueError:
        return messages.int_error('car_id and customer_id')
    
    return cancel_order(car_id, customer_id)
