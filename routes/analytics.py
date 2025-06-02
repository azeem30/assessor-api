from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_analytics_routes(app, db_pool):
    @app.route("/submitted_tests", methods=["GET"])
    def get_submitted_tests():
        """Returns the number of tests submitted by the user"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "No email in request" } ), 400
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select count(*) as submitted_tests
                        from responses
                        where student_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    result = cursor.fetchone()
                    submitted_tests = result["submitted_tests"]
                    return jsonify( { "submitted_tests": int(submitted_tests) } ), 200
            return jsonify( { "error": "An error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500

    @app.route("/average_score", methods=["GET"])
    def get_average_score():
        """Returns the average score of the user for all the tests"""
        try:
            email = request.args.get("email")
            if not email:
                return jsonify( { "error": "No email in request" } ), 400
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select marks_obtained as marks
                        from responses
                        where student_email = %s
                    """
                    data = (email, )
                    cursor.execute(query, data)
                    results = cursor.fetchall()

                    # Compute average score of the user
                    sum = 0
                    for result in results:
                        sum += int(result["marks"])
                    
                    average = sum / len(results)
                    return jsonify( { "average_score": average } ), 200
            return jsonify( { "error": "An error occured" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500
