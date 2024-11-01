"""from flask import jsonify
from project import driver, app


@app.route('/test')
def test_connection():
    try:
        with driver.session() as session:
            # Try a simple query to confirm connection
            result = session.run("RETURN 1 AS result")
            return jsonify({"status": "success", "result": result.single()["result"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})"""