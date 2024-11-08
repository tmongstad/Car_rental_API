from typing import Any
from flask import jsonify

def int_error(field_name: str):
    message = jsonify({
            "Status": "Error",
            "Message": f"The {field_name} field must be an integer."
        }), 400
    return message

def missing_field_error(missing_fields: str):
    message = jsonify({
            "Status": "Error",
            "Message": f"Missing required fields. Please provide {missing_fields}."
        }), 400
    return message

def success(node: str, key: str, value: Any, results, type_of_operation):
    message = jsonify({
            "Status": "Success",
            "Message": f"{node} with {key} {value} {type_of_operation} successfully.",
            f"data": results
        }), 200
    return message

def no_results(node: str, key: str, value: Any):   
    message = jsonify({
        "Status": "Error",
        "Message": f"No {node} found with {key}: {value}"
        }), 404
    return message

def check_results(node, key, value, data, operation):
    if data:
        return success(node, key, value, data, operation)
    else:
        return no_results(node, key, value)