from flask import Blueprint, request, jsonify
from app.controllers.student_controller import get_all_students, create_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/api/students', methods=['GET'])
def get_students():
    """
    Obtain students list (with pagination)
    ---
    tags:
      - Students
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Students per page
    responses:
      200:
        description: Paginated student list
        schema:
          type: object
          properties:
            students:
              type: array
              items:
                type: object
            total:
              type: integer
            page:
              type: integer
            total_pages:
              type: integer
    """
    # URL parameter obtain (?page=1&per_page=5)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    result = get_all_students(page, per_page)
    return jsonify(result), 200

@student_bp.route('/api/students', methods=['POST'])
def add_student():
    """
    Create new student
    ---
    tags:
      - Students
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
            - email
            - major
            - semester
            - enrollment_date
          properties:
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
            gpa:
              type: number
            enrollment_date:
              type: string
              format: date
              example: "2025-01-30"
    responses:
      201:
        description: Student created successfully.
      409:
        description: duplicated email.
    """
    data = request.get_json()
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
        return jsonify({"error": "Could not create student. Email might be duplicated."}), 409