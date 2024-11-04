from project.model.query_management import run_query
from project.model import messages
from flask import request

def add_employee():
    employee_data = request.get_json()
    name = employee_data['name'] # Gets the make from the posted JSON.
    branch = employee_data['branch']
    address = employee_data['address']
    if not name or not branch or not address:
        return messages.missing_field_error(missing_fields_as_string='name, branch and address')
    query = """
    CREATE (employee:Employee {name: $name, branch:$branch, address:$address})
    SET employee.employee_id = id(employee) 
    RETURN employee
    """
    returned_data = run_query(query, {'name':name, 'branch':branch, 'address':address}) # Runs the query, with the parameters provided
    return returned_data

def get_all_employees():
    query = "MATCH (employee:Employee) RETURN employee"
    data = run_query(query)
    if data:
        return data
    else:
        return "No data"

def get_employee(employee_id):
    try:
        employee_id = int(employee_id)
    except ValueError:
        return messages.int_error('employee_id')
    query = "MATCH (employee:Employee {employee_id:$employee_id}) RETURN employee"
    returned_data = run_query(query, {'employee_id':employee_id})
    return returned_data

def update_employee(employee_id):
    try:
        employee_id = int(employee_id)
    except ValueError:
        return messages.int_error('employee_id')
    data = request.get_json()
    fields = {}
    if 'name' in data:
        fields['name'] = data['name']
    if 'branch' in data:
        fields['branch'] = data['branch']
    if 'address' in data:
        fields['address'] = data['address']    
    query_variable = ','.join([f'employee.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (employee:Employee{{employee_id:$employee_id}})
    SET {query_variable}
    RETURN employee
    """
    results = run_query(query, {'employee_id':employee_id, **fields})
    if results:
        return messages.success('Employee', 'ID', employee_id, results[0], 'update')
    else:
        return messages.no_results('Employee', 'employee_id', employee_id)

def delete_employee(employee_id):
    try:
        employee_id = int(employee_id)
    except ValueError:
        return messages.int_error('employee_id')
    query = "MATCH (employee:Employee {employee_id:$employee_id}) DETACH DELETE employee RETURN COUNT(employee) AS deleted_count"
    result = run_query(query, {'employee_id':employee_id})
    return result
