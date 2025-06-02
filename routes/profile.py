from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_profile_routes(app, db_pool):
    @app.route("/update_user/<string:email>", methods=["PUT"])
    def update_user(email):
        try:
            data = request.get_json()
            if not data:
                return jsonify( { "error": "No data received" } ), 400
            new_email = data["email"]
            name = data["name"]
            department = data["department"]
            if not name:
                return jsonify( { "error": "Name cannot be empty" } ), 400
            if not department:
                return jsonify( { "error": "Department cannot be empty" } ), 400
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        update students
                        set
                        email = %s,
                        name = %s,
                        dept_name = %s
                        where email = %s
                    """
                    data = (new_email, name, department, email)
                    cursor.execute(query, data)
                    connection.commit()
                    return jsonify( { "message": "Profile updated successfully" } ), 200
            return jsonify( { "error": "An error occured updating profile" } ), 400 
        except Exception as e:
            print(str(e))
            return jsonify( { "error": str(e) } ), 500
