from flask import jsonify, request
from utils.db_utils import get_db_connection

def register_response_routes(app, db_pool):
    @app.route("/responses", methods=["GET"])
    def get_responses():
        try:
            student_email = request.args.get("email")
            if not student_email:
                return jsonify( { "error": "No email in the request" } ), 400
            with get_db_connection(db_pool) as connection:
                with connection.cursor() as cursor:
                    query = f"""
                        select 
                        t.id as test_id,
                        t.title,
                        t.subject,
                        t.marks as total_marks,
                        t.difficulty,
                        t.teacher_email,
                        t.pairs,
                        t.duration,
                        r.id,
                        r.marks_obtained,
                        r.submitted_at
                        from tests as t inner join responses as r
                        on t.id = r.test_id
                        where r.student_email = %s
                    """
                    data = (student_email, )
                    cursor.execute(query, data)
                    responses = cursor.fetchall()

                    for response in responses:
                        query = f"""
                            select
                            question,
                            sample_answer,
                            user_answer,
                            similarity,
                            marks
                            from response_data
                            where response_id = %s
                        """
                        data = (response["id"], )
                        cursor.execute(query, data)
                        questions_and_answers = cursor.fetchall()
                        response["questions_and_answers"] = questions_and_answers

                    return jsonify( { "responses": responses } ), 200
            return jsonify( { "error": "An error occured fetching responses" } ), 400
        except Exception as e:
            return jsonify( { "error": str(e) } ), 500
