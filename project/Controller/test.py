"""from project import app
from project.model.order_management import check_customer
from flask import request

@app.route('/test/check_customer/<customer_id>', methods = ['GET'])
def test_check_customer(customer_id):
    if request.method == 'GET':
        data = check_customer(customer_id)
        return data"""