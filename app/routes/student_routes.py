from flask import Blueprint, request, jsonify
from app.controllers.student_controller import get_all_students, create_student

# Define the Blueprint named 'student_bp'
student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/api/students', methods=['GET'])
def get_students():
    """
    Get all student list.
    ---
    tags:
      - Students
    responses:
      200:
        description: Full list of registered students
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              first_name:
                type: string
              last_name:
                type: string
              email:
                type: string
              major:
                type: string
              semester:
                type: integer
    """
    students = get_all_students()
    return jsonify(students), 200

@student_bp.route('/api/students', methods=['POST'])
def add_student():
    """
    Endpoint to create a new student.
    Expected Body: JSON with first_name, last_name, email, etc.
    """
    data = request.get_json()
    
    # Basic validation (Your teammate will add robust validations here later!)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_id = create_student(data)
    
    if new_id:
        return jsonify({
            "message": "Student created successfully",
            "id": new_id,
            "student": data
        }), 201
    else:
        # If ID is None, likely the email already exists
        return jsonify({"error": "Could not create student. Email might be duplicated."}), 409