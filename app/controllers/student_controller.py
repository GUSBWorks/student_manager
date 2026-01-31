import sqlite3
from app.database.db_config import get_db_connection

def get_all_students(page=1, per_page=10, is_active=True):
    """
    Retrieve students with pagination and active status filter.
    Args:
        is_active (bool/str): Filter by active status (True/False or 'true'/'false').
    """
    conn = get_db_connection()
    offset = (page - 1) * per_page
    
    # Convert string 'true'/'false' to boolean 1/0 for SQLite
    if str(is_active).lower() == 'false':
        status_filter = 0
    else:
        status_filter = 1
        
    try:
        # Filter dynamically based on user requests.
        count_sql = 'SELECT COUNT(*) FROM students WHERE is_active = ?'
        total_count = conn.execute(count_sql, (status_filter,)).fetchone()[0]
        
        sql = 'SELECT * FROM students WHERE is_active = ? LIMIT ? OFFSET ?'
        students = conn.execute(sql, (status_filter, per_page, offset)).fetchall()
        
        return {
            "students": [dict(row) for row in students],
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
    finally:
        conn.close()

def create_student(student_data):
    """
    Create a new student in the database.
    Args:
        student_data (dict): Dictionary containing student info.
    Returns:
        int: The ID of the new student, or None if error.
    """
    conn = get_db_connection()
    try:
        sql = '''
            INSERT INTO students (first_name, last_name, email, major, semester, gpa, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = conn.execute(sql, (
            student_data['first_name'],
            student_data['last_name'],
            student_data['email'],
            student_data['major'],
            student_data['semester'],
            student_data['gpa'],
            student_data['enrollment_date']
        ))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.IntegrityError as e:
        # This usually happens if email is not unique
        print(f"Integrity Error: {e}")
        return None
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None
    finally:
        conn.close()

def get_student_by_id(student_id):
    """
    Retrieve a single student by ID (Only if active).
    """
    conn = get_db_connection()
    try:
        
        sql = 'SELECT * FROM students WHERE id = ? AND is_active = 1'
        student = conn.execute(sql, (student_id,)).fetchone()
        
        if student:
            return dict(student)
        return None
    finally:
        conn.close()

def update_student(student_id, data):
    """
    Update student data (Dynamic SQL for both PUT and PATCH).
    Returns: Updated student dict or None if not found.
    """
    conn = get_db_connection()
    try:
        # Check if student exists
        student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
        if not student:
            conn.close()
            return None

        # Build dynamic query: "UPDATE students SET field1=?, field2=? WHERE id=?"
        fields = []
        values = []
        for key, value in data.items():
            # Only update valid columns and update 'updated_at' automatically
            if key in ['first_name', 'last_name', 'email', 'major', 'semester', 'gpa', 'is_active']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        fields.append("updated_at = CURRENT_TIMESTAMP")
        
        if not fields:
            conn.close()
            return dict(student) # Nothing to update

        sql = f"UPDATE students SET {', '.join(fields)} WHERE id = ?"
        values.append(student_id)
        
        conn.execute(sql, values)
        conn.commit()
        
        # Return the updated student
        updated_student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
        return dict(updated_student)
    finally:
        conn.close()

def delete_student(student_id):
    """Soft delete a student (set is_active = 0)."""
    conn = get_db_connection()
    try:
        # Check if exists first
        student = conn.execute('SELECT id FROM students WHERE id = ?', (student_id,)).fetchone()
        if not student:
            return False
            
        conn.execute('UPDATE students SET is_active = 0 WHERE id = ?', (student_id,))
        conn.commit()
        return True
    finally:
        conn.close()


def restore_student(student_id):
    """Restore a soft-deleted student (set is_active = 1)."""
    conn = get_db_connection()
    try:
        # Verificamos si existe (incluso si está borrado)
        student = conn.execute('SELECT id FROM students WHERE id = ?', (student_id,)).fetchone()
        if not student:
            return False
            
        conn.execute('UPDATE students SET is_active = 1 WHERE id = ?', (student_id,))
        conn.commit()
        return True
    finally:
        conn.close()



#FUNCTION GET ALL STUDENT WITH NO RETRIEVE INACTIVES
    # def get_all_students(page=1, per_page=10):
    # """
    # Retrieve ONLY ACTIVE students with pagination.
    # Args:
    #     page (int): Page number (default 1).
    #     per_page (int): Number of items per page (default 10).
    # """
    # conn = get_db_connection()
    # offset = (page - 1) * per_page
    
    # try:
    #     # Only count those that are active (is_active = 1)
    #     total_count = conn.execute('SELECT COUNT(*) FROM students WHERE is_active = 1').fetchone()[0]
        
    #     # Only bring in those that are active
    #     sql = 'SELECT * FROM students WHERE is_active = 1 LIMIT ? OFFSET ?'
    #     students = conn.execute(sql, (per_page, offset)).fetchall()
        
    #     return {
    #         "students": [dict(row) for row in students],
    #         "total": total_count,
    #         "page": page,
    #         "per_page": per_page,
    #         "total_pages": (total_count + per_page - 1) // per_page
    #     }
    # except sqlite3.Error as e:
    #     print(f"Database error: {e}")
    #     return {"students": [], "total": 0}
    # finally:
    #     conn.close()