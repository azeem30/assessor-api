import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import jsonify, request
from utils.db_utils import get_db_connection
from utils.test_utils import filter_submitted_tests
from utils.resp_utils import generate_response_id
from utils.resp_utils import calculate_marks

def register_test_routes(app, model, db_pool):
    @app.route("/tests", methods=["GET"])
    def get_tests():
        try:
            # Validate the data in the request
            student_email = request.args.get("email", "")
            if not student_email:
                return jsonify( { "error": "No email in the request" } ), 400
            department = request.args.get("department", "")
            if not department:
                return jsonify( { "error": "No department in the request" } ), 400

            # Query the available tests for the user
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    # Query the tests scheduled for the department
                    query = f"""
                        select 
                        t.id,
                        t.title,
                        t.subject,
                        t.duration,
                        t.marks,
                        t.difficulty,
                        t.scheduled_at,
                        t.pairs,
                        t.teacher_email
                        from tests as t
                        where t.dept_name = %s
                    """
                    data = (department, )
                    cursor.execute(query, data)
                    tests = cursor.fetchall()
                    
                    # Query the tests that are already submitted by the user
                    query = f"""
                        select test_id
                        from responses
                        where student_email = %s
                    """
                    data = (student_email, )
                    cursor.execute(query, data)
                    responses = cursor.fetchall()
                    
                    # Filter out the submitted tests
                    available_tests = filter_submitted_tests(tests, responses)
                    
                    for test in available_tests:
                        query = f"""
                            select question, answer
                            from questions_and_answers
                            where id = %s
                        """
                        data = (test["id"], )
                        cursor.execute(query, data)
                        questions_and_answers = cursor.fetchall()
                        test["questions_and_answers"] = questions_and_answers

                    return jsonify( { "tests": available_tests } ), 200
            return jsonify( { "error": "An error occured fetching available tests" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500

    @app.route("/save_response", methods=["POST"])
    def save_response():
        try:
            # Validation of the data received in the request
            data = request.get_json()
            if not data:
                return jsonify( { "error": "No data provided" } ), 400
            student_email = data["email"]
            test_id = data["test_id"]
            questions_and_answers = data["questions_and_answers"]
            
            id = generate_response_id()
            qna_with_marks, total_marks = calculate_marks(model, questions_and_answers)
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        insert into responses
                        (id, student_email, test_id, marks_obtained)
                        values
                        (%s, %s, %s, %s)
                    """
                    data = (id, student_email, test_id, total_marks)
                    cursor.execute(query, data)
                    connection.commit()
                    
                    for item in qna_with_marks:
                        query = f"""
                            insert into response_data
                            (question, sample_answer, user_answer, response_id, similarity, marks) 
                            values
                            (%s, %s, %s, %s, %s, %s)
                        """
                        data = (item["question"], item["sampleAnswer"], item["userAnswer"], id, item["similarity"], item["marks"])
                        cursor.execute(query, data)
                        connection.commit()

                    return jsonify( { "message": "Response saved successfully" } ), 200
            return jsonify( { "error": "Error saving response" } ), 400
        except Exception as e:
            print(str(e))
            return jsonify( { "error": str(e) } ), 500
