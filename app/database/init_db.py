import sqlite3

# Name of the database
DB_NAME = "students.db"

def init_db():
    """Initialize the database with the students table."""
    # Connect with DB (in case db doesn't exist its gonna create it.)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Now we make the instructions for the SQL Table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        major VARCHAR(100) NOT NULL,
        semester INTEGER NOT NULL,
        gpa DECIMAL(3,2),
        enrollment_date DATE NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Success: Database initialized and table 'students' created.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# This line its for directly execute the file.
if __name__ == "__main__":
    init_db()