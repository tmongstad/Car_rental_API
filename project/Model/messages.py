from flask import jsonify

def int_error(variable):
    return jsonify({
            "Status": "Error",
            "Message": f"The {variable} field must be an integer."
        }), 400

def missing_field_error(variable):
    message = jsonify({
            "Status": "Error",
            "Message": f"Missing required fields. Please provide {variable}."
        }), 400
    return 
    