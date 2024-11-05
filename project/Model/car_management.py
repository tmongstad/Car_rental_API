from flask import request, jsonify
from project.model.query_management import run_query
from project.model import messages

def get_all_cars():
    query = "MATCH (car:Car) RETURN car"
    data = run_query(query)
    return data

def add_car(make, model, year, location, status):
    query = """
    CREATE (car:Car {make: $make, model:$model, year:$year, location:$location, status:$status})
    SET car.car_id = id(car) 
    RETURN car
    """
    car_data = run_query(query, {'make':make, 'model':model, 'year':year, 'location':location, 'status':status}) # Runs the query, with the parameters provided
    if car_data:
        return car_data[0]['car']
    else:
        return []

def get_car(car_id):
    query = "MATCH (car:Car{car_id:$car_id}) RETURN car"
    car_data = run_query(query, params={'car_id':car_id})
    if car_data:
        return car_data[0]['car']
    else:
        return []

def update_car(car_id, fields):
    query_variable = ','.join([f'car.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (car:Car{{car_id:$car_id}})
    SET {query_variable}
    RETURN car
    """
    car_data = run_query(query, {'car_id':car_id, **fields})
    if car_data:
        return car_data[0]['car']
    else:
        return []

def delete_car(car_id):
    car_data = get_car(car_id)
    if car_data: 
        if car_data['status']== 'available':
            query = "MATCH (car:Car {car_id:$car_id}) DETACH DELETE car RETURN COUNT(car) AS deleted_count"
            result = run_query(query, {'car_id':car_id})
            if result[0]['deleted_count'] == 1:
                return {'deleted_car': car_data} # Returns the deleted car data
            else:
                return [] # If the query fails.
        else:
            return {'Car_status': 'The car is unavailable'} # If the car is not available
    else:
        return [] # If no car is found