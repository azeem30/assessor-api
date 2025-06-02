import uuid
import base64

def generate_response_id():
    """Generates an unique ID for the response"""
    try:
        unique_bytes = uuid.uuid4().bytes[:6]
        unique_str = base64.urlsafe_b64encode(unique_bytes).decode("utf-8").rstrip("=")
        return unique_str
    except Exception as e:
        raise e

def convert_similarity_to_grade(similarity):
    try:
        if 0 < similarity and similarity <= 10:
            return 1
        elif 10 < similarity and similarity <= 20:
            return 2
        elif 20 < similarity and similarity <= 30:
            return 3
        elif 30 < similarity and similarity <= 40:
            return 4
        elif 40 < similarity and similarity <= 50:
            return 5
        elif 50 < similarity and similarity <= 60:
            return 6
        elif 60 < similarity and similarity <= 70:
            return 7
        elif 70 < similarity and similarity <= 80:
            return 8
        elif 80 < similarity and similarity <= 90:
            return 9
        elif 90 < similarity and similarity <= 100:
            return 10
        elif similarity > 100:
            return 10
        return 0
    except Exception as e:
        raise e

def calculate_marks(model, questions_and_answers):
    try:
        total = 0
        for item in questions_and_answers:
            similarity = model.compute_final_score(item["sampleAnswer"], item["userAnswer"])
            item["similarity"] = similarity
            item["marks"] = convert_similarity_to_grade(similarity)
            total += item["marks"]
        return questions_and_answers, total
    except Exception as e:
        raise e
