from project.model.employee_management import get_all_employees, add_employee, get_employee, update_employee, delete_employee
from flask import request
from project import app
from project.model import messages


@app.route('/employee', methods = ['GET', 'POST'])
def manage_employee():
    # Gets all employees:
    if request.method == 'GET':
        employee_data = get_all_employees()
        return messages.check_results('Employees', 'All employee data', '', employee_data, 'recieved')
    
    # Adds a new employee:
    if request.method == 'POST':
        employee_data = request.get_json() # Gets input from user and converts to dict
        name = employee_data['name'] 
        branch = employee_data['branch']
        address = employee_data['address']
        if not name or not branch or not address:
            return messages.missing_field_error(missing_fields_as_string='name, branch and address') # Retrurns error if one of the fields are missing.   
        employee_data = add_employee(name, branch, address)
        return messages.check_results('Employee', 'employee_id', employee_data['employee_id'], employee_data, 'added')

# Route for getting, updating and deleting specific car-data
@app.route('/employee/<employee_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_employees(employee_id):
    # Checks the user input:
    try:
        employee_id = int(employee_id)
    except ValueError:
        return messages.int_error('employee_id')
    
    # gets employee by id:
    if request.method == 'GET':
        employee_data = get_employee(employee_id)
        return messages.check_results('Employee', 'employee ID', employee_id, employee_data, 'found')
    
    # Edits an employee:
    if request.method == 'PUT':
        data = request.get_json()
        fields = {}
        if 'name' in data:
            fields['name'] = data['name']
        if 'branch' in data:
            fields['branch'] = data['branch']
        if 'address' in data:
            fields['address'] = data['address']    
        employee_data = update_employee(fields, employee_id)
        return messages.check_results('Employee', 'employee ID', employee_id, employee_data, 'updated')
    
    # Deletes an employee:
    if request.method == 'DELETE':
        data = delete_employee(employee_id)
        return messages.check_results('Employee', 'employee ID', employee_id, data, 'Deleted')