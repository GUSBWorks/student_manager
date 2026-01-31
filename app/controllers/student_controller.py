import sqlite3
from app.database.db_config import get_db_connection

def get_all_students(page=1, per_page=10):
    """
    Retrieve students with pagination.
    Args:
        page (int): Page number (default 1).
        per_page (int): Number of items per page (default 10).
    """
    conn = get_db_connection()
    offset = (page - 1) * per_page
    
    try:
        # Total count to know how much pages are. 
        total_count = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        
        # Bring only what we need (LIMIT and OFFSET)
        sql = 'SELECT * FROM students LIMIT ? OFFSET ?'
        students = conn.execute(sql, (per_page, offset)).fetchall()
        
        return {
            "students": [dict(row) for row in students],
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page
        }
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"students": [], "total": 0}
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