from flask import request, jsonify
from project.model.query_management import run_query
from project.model import messages

def get_all_cars():
    query = "MATCH (car:Car) RETURN car"
    data = run_query(query)
    return data

def add_car():
    data = request.get_json()
    make = data.get('make') # Gets the make from the posted JSON.
    model = data.get('model')
    year = data.get('year')
    location = data.get('location')
    status = data.get('status')
    if not make or not model or not year or not location or not status:
        return jsonify({
            "Status": "Error",
            "Message": "Missing required fields. Please provide 'make', 'model', 'year', 'location' and 'status'."
        }), 400
        # return messages.int_error('m')
    try:
        year = int(year)
    except ValueError:
        """return jsonify({
            "Status": "Error",
            "Message": "The 'year' field must be an integer."
        }), 400"""
        return messages.int_error(year)
    query = """
    CREATE (car:Car {make: $make, model:$model, year:$year, location:$location, status:$status})
    SET car.car_id = id(car) 
    RETURN car
    """
    returned_data = run_query(query, {'make':make, 'model':model, 'year':year, 'location':location, 'status':status}) # Runs the query, with the parameters provided
    
    return jsonify({
        "Status": "Success",
        "Message": "Car added successfully.",
        "Car":returned_data
        }), 201

def get_car(car_id):
    query = "MATCH (car:Car{car_id:$car_id}) RETURN car"
    results = run_query(query, params={'car_id':car_id})
    return results[0]['car']
    if results:
        return jsonify({ # Return this dict in a json-format.
            'Status': 'Success!',
            'data': results
        }), 200  # Status code that tells us that the requested resource was found
    else:
        return jsonify({ # Return this dict in a json-format.
            "Status": "Error",
            "Message": f"No cars found with car_id: {car_id}"
        }), 404  # Status code that tells us that it was not found

def update_car(car_id, fields):
    query_variable = ','.join([f'car.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (car:Car{{car_id:$car_id}})
    SET {query_variable}
    RETURN car
    """
    updated_data = run_query(query, {'car_id':car_id, **fields})
    return updated_data
    
def delete_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify('Not an integer')
    query = "MATCH (car:Car {car_id:$car_id}) DETACH DELETE car RETURN COUNT(car) AS deleted_count"
    result = run_query(query, {'car_id':car_id})
    return result