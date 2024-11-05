from project.model.car_management import add_car, get_car, update_car, delete_car, run_query, get_all_cars
from flask import jsonify, request
from project import app
from project.model import messages

# Route for getting all cardata and adding car data
@app.route('/cars', methods = ['GET', 'POST'])
def manage_cars():
    # Gets all cars
    if request.method == 'GET':
        data = get_all_cars()
        return messages.check_results('All cars', 'none', 'none', data, 'found')
    
    # Adds a car
    if request.method == 'POST':
        data = request.get_json()
        make = data.get('make') # Gets the make from the posted JSON.
        model = data.get('model')
        year = data.get('year')
        location = data.get('location')
        status = data.get('status')
        if not make or not model or not year or not location or not status:
            return messages.missing_field_error("'make', 'model', 'year', 'location' or 'status'")
        try:
            year = int(year)
        except ValueError:
            return messages.int_error('year')
        data = add_car(make, model, year, location, status)
        return messages.check_results('Car', 'Car_id', data['car_id'], data, 'added')

# Route for getting, updating and deleting specific car-data
@app.route('/cars/<car_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_cars(car_id):
    #Checks the user input
    try:
        car_id = int(car_id)
    except ValueError:
        return messages.int_error('car_id')
    
    # Finds a car by id
    if request.method == 'GET':
        results = get_car(car_id)
        return messages.check_results('car', 'car_id', car_id, results, 'found')
        
    # Updates the car
    if request.method == 'PUT':
        data = request.get_json()
        fields = {}
        if 'make' in data:
            fields['make'] = data['make']
        if 'model' in data:
            fields['model'] = data['model']
        if 'location' in data:
            fields['location'] = data['location']
        if 'year' in data:
            try:
                data['year'] = int(data['year'])
            except ValueError:
                return messages.int_error('year')
            fields['year'] = data['year']
        if 'status' in data:
            fields['status'] = data['status']
        data = update_car(car_id, fields)
        return messages.check_results('car', 'car_id', car_id, data, 'updated')
        

    # Deletes a car
    if request.method == 'DELETE':
        results = delete_car(car_id)
        if results == {'Car_status': 'The car is unavailable'}:
            return jsonify({
                    "Message": f"Car with ID: {car_id} is unavailable",
                    "Status": "Fail",
                    })
        return messages.check_results('car', 'car_id', car_id, results, 'deleted')
        
