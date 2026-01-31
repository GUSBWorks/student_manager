import sqlite3
from app.database.db_config import get_db_connection

def get_all_students():
    """
    Retrieve all students from the database.
    Returns: List of dictionaries representing students.
    """
    conn = get_db_connection()
    try:
        students = conn.execute('SELECT * FROM students').fetchall()
        # Convert sqlite3.Row objects to standard dictionaries
        return [dict(row) for row in students]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
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