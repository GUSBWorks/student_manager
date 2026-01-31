from flask import Blueprint, request, jsonify
from app.controllers.student_controller import (
    get_all_students, create_student, get_student_by_id, 
    update_student, delete_student
)
from app.utils.validators import validate_student_data

student_bp = Blueprint('student_bp', __name__)

# --- PART A ENDPOINTS (GET ALL y POST) ---
@student_bp.route('/api/students', methods=['GET'])
def get_students():
    """
    Obtain students list (with pagination)
    ---
    tags: [Students]
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Paginated list
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result = get_all_students(page, per_page)
    return jsonify(result), 200

@student_bp.route('/api/students', methods=['POST'])
def add_student():
    """
    Create new student
    ---
    tags: [Students]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [first_name, last_name, email, major, semester, enrollment_date]
          properties:
            first_name: {type: string}
            last_name: {type: string}
            email: {type: string}
            major: {type: string}
            semester: {type: integer}
            gpa: {type: number}
            enrollment_date: {type: string}
    responses:
      201: {description: Created}
      400: {description: Invalid Data}
      409: {description: Email Conflict}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # VALIDATION
    is_valid, error_msg = validate_student_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    new_id = create_student(data)
    if new_id:
        return jsonify({"message": "Student created", "id": new_id, "student": data}), 201
    else:
        return jsonify({"error": "Email already exists"}), 409

# --- NEW ENDPOINTS (PART B) ---

@student_bp.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    """
    Obtain student by ID
    ---
    tags: [Students]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Student information
      404:
        description: Student not found
    """
    student = get_student_by_id(id)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@student_bp.route('/api/students/<int:id>', methods=['PUT'])
def update_student_full(id):
    """
    Update all student information (PUT)
    ---
    tags: [Students]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            first_name: {type: string}
            last_name: {type: string}
            email: {type: string}
            major: {type: string}
            semester: {type: integer}
            gpa: {type: number}
    responses:
      200: {description: Updated}
      400: {description: Validation Error}
      404: {description: Not Found}
    """
    data = request.get_json()
    
    # Validation (is_update=True allows partial checks logic, but PUT usually expects all fields. 
    # For simplicity, we just check data validity like GPA range)
    is_valid, error_msg = validate_student_data(data, is_update=True)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    updated_student = update_student(id, data)
    if updated_student:
        return jsonify({"message": "Student updated", "student": updated_student}), 200
    return jsonify({"error": "Student not found"}), 404

@student_bp.route('/api/students/<int:id>', methods=['PATCH'])
def update_student_partial(id):
    """
    Partly update student(PATCH)
    ---
    tags: [Students]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          properties:
            major: {type: string}
            gpa: {type: number}
    responses:
      200: {description: Updated}
    """
    data = request.get_json()
    is_valid, error_msg = validate_student_data(data, is_update=True)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    updated_student = update_student(id, data)
    if updated_student:
        return jsonify({"message": "Student updated", "student": updated_student}), 200
    return jsonify({"error": "Student not found"}), 404

@student_bp.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student_record(id):
    """
    Students soft delete (Soft Delete)
    ---
    tags: [Students]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Student deleted (inactive)}
      404: {description: Not found}
    """
    success = delete_student(id)
    if success:
        return jsonify({"message": "Student deleted successfully"}), 200
    return jsonify({"error": "Student not found"}), 404












# --------------------- BEFORE ADDING THE PART B ------------------------- #


# from flask import Blueprint, request, jsonify
# from app.controllers.student_controller import get_all_students, create_student

# student_bp = Blueprint('student_bp', __name__)

# @student_bp.route('/api/students', methods=['GET'])
# def get_students():
#     """
#     Obtain students list (with pagination)
#     ---
#     tags:
#       - Students
#     parameters:
#       - name: page
#         in: query
#         type: integer
#         default: 1
#         description: Page number
#       - name: per_page
#         in: query
#         type: integer
#         default: 10
#         description: Students per page
#     responses:
#       200:
#         description: Paginated student list
#         schema:
#           type: object
#           properties:
#             students:
#               type: array
#               items:
#                 type: object
#             total:
#               type: integer
#             page:
#               type: integer
#             total_pages:
#               type: integer
#     """
#     # URL parameter obtain (?page=1&per_page=5)
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)
    
#     result = get_all_students(page, per_page)
#     return jsonify(result), 200

# @student_bp.route('/api/students', methods=['POST'])
# def add_student():
#     """
#     Create new student
#     ---
#     tags:
#       - Students
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           type: object
#           required:
#             - first_name
#             - last_name
#             - email
#             - major
#             - semester
#             - enrollment_date
#           properties:
#             first_name:
#               type: string
#             last_name:
#               type: string
#             email:
#               type: string
#             major:
#               type: string
#             semester:
#               type: integer
#             gpa:
#               type: number
#             enrollment_date:
#               type: string
#               format: date
#               example: "2025-01-30"
#     responses:
#       201:
#         description: Student created successfully.
#       409:
#         description: duplicated email.
#     """
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     new_id = create_student(data)
    
#     if new_id:
#         return jsonify({
#             "message": "Student created successfully",
#             "id": new_id,
#             "student": data
#         }), 201
#     else:
#         return jsonify({"error": "Could not create student. Email might be duplicated."}), 409