from project.model.car_management import add_car, get_car, update_car, delete_car, run_query, get_all_cars
from flask import jsonify, request
from project import app


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
    if request.method == 'GET':
        return get_car(car_id)
    if request.method == 'PUT':
        return update_car(car_id)
    if request.method == 'DELETE':
        return delete_car(car_id)