from project.model.query_management import run_query
from project.model import messages
from flask import request

def get_all_employees():
    query = "MATCH (employee:Employee) RETURN employee"
    data = run_query(query)
    return data # Returns a list of all employees [{'employee':{'customer_1': 1}}, {'employee':{'customer_2': 1}}...]

def add_employee(name, branch, address):
    query = """
    CREATE (employee:Employee {name: $name, branch:$branch, address:$address})
    SET employee.employee_id = id(employee) 
    RETURN employee
    """
    employee_data = run_query(query, {'name':name, 'branch':branch, 'address':address}) # Runs the query, with the parameters provided
    if employee_data:
        return employee_data[0]['employee'] # Returns a dict: {'name':name, 'branch':branch, 'address':address}
    else:
        return []

def get_employee(employee_id):
    query = "MATCH (employee:Employee {employee_id:$employee_id}) RETURN employee"
    employee_data = run_query(query, {'employee_id':employee_id})
    if employee_data:
        return employee_data[0]['employee'] # Returns a dict: {'name':name, 'branch':branch, 'address':address}
    else:
        return []
def update_employee(fields, employee_id):
    query_variable = ','.join([f'employee.{key}=${key}' for key in fields.keys()])
    query = f"""
    MATCH (employee:Employee{{employee_id:$employee_id}})
    SET {query_variable}
    RETURN employee
    """
    employee_data = run_query(query, {'employee_id':employee_id, **fields})
    if employee_data:
        return employee_data[0]['employee'] # Returns a dict: {'name':name, 'branch':branch, 'address':address}
    else:
        return []
def delete_employee(employee_id):
    employee_data = get_employee(employee_id)
    if employee_data:
        query = "MATCH (employee:Employee {employee_id:$employee_id}) DETACH DELETE employee RETURN COUNT(employee) AS deleted_count"
        result = run_query(query, {'employee_id':employee_id})
        if result[0]['deleted_count'] == 1:
            return {'deleted_employee': employee_data}
        else:
            return [] # If query fails
    else:
        return [] # If employeedata not found
