from project.model.order_management import generate_order, cancel_order, get_order_by_customer, get_all_orders, change_booking_status, returned_car
from flask import request, jsonify
from project import app
from project.model import messages
from project.model.customer_management import get_customer
from project.model.car_management import get_car, update_car

@app.route('/get_orders', methods = ['GET'])
def all_orders():
    order_data = get_all_orders()
    return messages.success('Order', '', '', order_data, 'recieved')

@app.route('/order_car', methods = ['POST'])
def order_car():
    # Gets the needed data
    user_data = request.get_json()
    car_id = user_data.get('car_id')
    customer_id = user_data.get('customer_id')
    if car_id is None or customer_id is None:
        return messages.missing_field_error('car id or customer id')
    # Checks the input
    try: 
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('customer_id and car_id')
    customer_data = get_customer(customer_id)  # Gets customer data
    car_data = get_car(car_id) # Gets car_data
    if customer_data is None: # Returns error-message if customer is not found
        return messages.no_results('Customer', 'customer_id', customer_id)
    if car_data is None: # Returns error-message if car is not found
        return messages.no_results('Car', 'car_id', car_id)
    # Checks if a customer already has placed an order.
    customer_booked = get_order_by_customer(customer_id)
    if customer_booked:
        return jsonify({
            'Message': 'Customer already has placed an order',
            'Status': 'Unable',
            'Data': customer_booked
        })
    # Checks if the car is available.
    if car_data['status'] != 'available':
        return jsonify({
            'Message': f'Car is Not available',
            'Status':'not available',
            'Data': car_data
        })            
    # Checks if the car is available
    else:
        update_car(car_id, {'status': 'booked'})
        order_data = generate_order(customer_id, car_id)
        return order_data#messages.success('Order', 'Order ID', order_data[0]['order']['order_id'], order_data, 'generated')
    

@app.route('/rent_car', methods = ['PUT'])
def rent_car():
    data = request.get_json()
    car_id, customer_id = data.get('car_id'), data.get('customer_id')
    if car_id is None or customer_id is None:
        return messages.missing_field_error('car id or customer id')
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('car_id and customer_id')
    car_data = change_booking_status(car_id, 'rented')
    return messages.check_results('Car', 'car ID', car_id, car_data, 'updated')

@app.route('/return_car', methods = ['PUT']) # Gets car_id, customer_id, and sets status to 'waiting for damage report'
def return_car():
    data = request.get_json()
    car_id, customer_id, car_status = data.get('car_id'), data.get('customer_id'), data.get('car_status')
    if car_id is None or customer_id is None or car_status is None:
        return messages.missing_field_error('car_id, customer_id or car_status')
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('car_id and customer_id')
    if car_status.lower() in ['ok', 'damaged']:
        if car_status.lower() == 'damaged':
            cancel_order(car_id, customer_id)
            car_data = update_car(car_id, {'status': 'damaged'})
            return jsonify({
                'message': 'Car needs to be fixed',
                'status': 'damaged',
                'Data': car_data
            })
        if car_status.lower() == 'ok':
            car_data = returned_car(car_id, customer_id)
            return messages.check_results('Customer', 'Customer_id', customer_id, car_data, f'returned car with id{car_id}')
    else:
        return jsonify({
            'message': 'status must be either OK or damaged',
            'Status': 'error'
        })

@app.route('/fix_car', methods=['PUT'])
def fix_car():
    data = request.get_json()
    car_id = data.get('car_id')
    if car_id is None:
        return messages.missing_field_error('car_id')
    try:
        car_id = int(car_id)
    except ValueError:
        return messages.int_error('car_id')
    car_data = update_car(car_id, {'status': 'available'})
    return messages.check_results('Car', 'car_id', car_id, car_data, 'fixed')

@app.route('/cancel_order_car', methods = ['DELETE'])
def cancel_order_car():
    data = request.get_json()
    car_id, customer_id = data.get('car_id'), data.get('customer_id')
    if car_id is None or customer_id is None:
        return messages.missing_field_error('car id or customer id')
    try:
        car_id = int(car_id)
        customer_id = int(customer_id)
    except ValueError:
        return messages.int_error('car_id and customer_id')
    order_data = cancel_order(car_id, customer_id) # Cancels the order.
    return messages.check_results('Order', 'Connected to', f'car: {car_id} and customer: {customer_id}', order_data, 'canceled')

