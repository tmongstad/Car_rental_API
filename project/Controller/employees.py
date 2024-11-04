from project.model.employee_management import get_all_employees, add_employee, get_employee, update_employee, delete_employee
from flask import request
from project import app


@app.route('/employee', methods = ['GET', 'POST'])
def manage_employee():
    if request.method == 'GET':
        return get_all_employees()
    if request.method == 'POST':
        return add_employee()

# Route for getting, updating and deleting specific car-data
@app.route('/employee/<employee_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_employees(employee_id):
    if request.method == 'GET':
        return get_employee(employee_id)
    if request.method == 'PUT':
        return update_employee(employee_id)
    if request.method == 'DELETE':
        return delete_employee(employee_id)