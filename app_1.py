from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# DATABASE URI and login-details
NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = 'admin123'

# Initiate driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

#Function that runs queries
def run_query(query, params = None):
    with driver.session() as session:
        result = session.run(query, params)
        return result.data()

# For testing connection
@app.route('/test')
def test_connection():
    try:
        with driver.session() as session:
            # Try a simple query to confirm connection
            result = session.run("RETURN 1 AS result")
            return jsonify({"status": "success", "result": result.single()["result"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Searches for specific car by 'make' return the result as JSON
@app.route('/search', methods = ['POST'])
def search():
    data = request.get_json() # Gets input in json-format.
    make = data.get('make') # Gets whats in the make-key
    query = """  
    MATCH (car:Car {make: $make}) RETURN car.make AS make, car.model AS model, car.year AS year, car.loc AS location
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
# Respons

# Gets all cars from database
def get_all_cars():
    query = "MATCH (car:Car) RETURN car"
    data = run_query(query)
    return data

# Adds a new car to the database
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
    try:
        year = int(year)
    except ValueError:
        return jsonify({
            "Status": "Error",
            "Message": "The 'year' field must be an integer."
        }), 400
    
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
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({
            "Status": "Error",
            "Message": "The 'car_id' field must be an integer."
        }), 400
    query = "MATCH (car:Car{car_id:$car_id}) RETURN car"
    results = run_query(query, params={'car_id':car_id})
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

def update_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({
            "Status": "Error",
            "Message": "The 'car_id' field must be an integer."
        }), 400
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
            return jsonify({
            "Status": "Error",
            "Message": "The 'car_id' field must be an integer."
        }), 400
        fields['year'] = data['year']
    if 'status' in data:
        fields['status'] = data['status']
    query_variable = ','.join([f'car.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (car:Car{{car_id:$car_id}})
    SET {query_variable}
    RETURN car
    """
    results = run_query(query, {'car_id':car_id, **fields})
    if results:
        return jsonify({
            "Status": "Success",
            "Message": f"Car with ID {car_id} updated successfully.",
            "Updated Data": results[0]
        }), 200
    else:
        return jsonify({
            "Status": "Error",
            "Message": f"No car found with car_id: {car_id}"
        }), 404
    
def delete_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify('Not an integer')
    query = "MATCH (car:Car {car_id:$car_id}) DETACH DELETE car RETURN COUNT(car) AS deleted_count"
    result = run_query(query, {'car_id':car_id})
    return result

if __name__ == '__main__':
    app.run(debug=True)
