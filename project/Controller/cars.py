from project.model.car_management import add_car, get_car, update_car, delete_car, run_query, get_all_cars
from flask import jsonify, request
from project import app
from project.model import messages


@app.route('/search', methods = ['POST'])
def search():
    data = request.get_json() # Gets input in json-format.
    make = data.get('make') # Gets whats in the make-key
    query = """  
    MATCH (car:Car {make: $make}) RETURN car.make AS make, car.model AS model, car.year AS year, car.location AS location
    """  # $ - allows to put variables into the query.
    results = run_query(query, {'make': make})

    if results:
        return jsonify({ # Return this dict in a json-format.
            'Status': 'Success!',
            'data': results
        }), 200  # Status code that tells us that the requested resource was found
    else:
        return jsonify({ # Return this dict in a json-format.
            "Status": "Error",
            "Message": f"No cars found with make: {make}"
        }), 404  # Status code that tells us that it was not found

# Route for getting all cardata and adding car data
@app.route('/cars', methods = ['GET', 'POST'])
def manage_cars():
    if request.method == 'GET':
        return get_all_cars()
    if request.method == 'POST':
        return add_car()

# Route for getting, updating and deleting specific car-data
@app.route('/cars/<car_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_cars(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return messages.int_error('car_id')
    if request.method == 'GET':
        return get_car(car_id)
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
        if data:
            return messages.success('Car', 'ID', car_id, data, 'update')
    if request.method == 'DELETE':
        return delete_car(car_id)