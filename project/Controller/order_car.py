from project.model.order_management import generate_order
from flask import request
from project import app
from project.model import messages

@app.route('/order_car', methods = ['POST'])
def order_car():
    order = generate_order()
    return order