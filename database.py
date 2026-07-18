import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            Admin_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    ''')

    # Create Student Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Semester INTEGER NOT NULL,
            Face_Embedding TEXT,
            Image_Path TEXT
        )
    ''')

    # Create Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            Attendance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_ID INTEGER NOT NULL,
            Date TEXT NOT NULL,
            Time TEXT NOT NULL,
            Status TEXT DEFAULT 'Present',
            FOREIGN KEY (Student_ID) REFERENCES Student (Student_ID)
        )
    ''')

    # Insert default admin if not exists
    cursor.execute("SELECT * FROM Admin WHERE Username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO Admin (Username, Password) VALUES (?, ?)", ('admin', hashed_pw))

    conn.commit()
    conn.close()

def verify_admin(username, password):
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM Admin WHERE Username = ?', (username,)).fetchone()
    conn.close()
    if admin and check_password_hash(admin['Password'], password):
        return True
    return False

def add_student(name, department, semester, embedding, image_path):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Student (Name, Department, Semester, Face_Embedding, Image_Path) VALUES (?, ?, ?, ?, ?)',
        (name, department, semester, embedding, image_path)
    )
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Student').fetchall()
    conn.close()
    return students

def mark_attendance(student_id):
    conn = get_db_connection()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Prevent duplicate attendance
    existing = conn.execute(
        'SELECT * FROM Attendance WHERE Student_ID = ? AND Date = ?', 
        (student_id, today)
    ).fetchone()
    
    if not existing:
        current_time = datetime.now().strftime('%H:%M:%S')
        conn.execute(
            'INSERT INTO Attendance (Student_ID, Date, Time, Status) VALUES (?, ?, ?, ?)',
            (student_id, today, current_time, 'Present')
        )
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_attendance_records(search_query="", date_filter=""):
    conn = get_db_connection()
    query = '''
        SELECT a.Attendance_ID, s.Name, s.Department, s.Semester, a.Date, a.Time, a.Status 
        FROM Attendance a
        JOIN Student s ON a.Student_ID = s.Student_ID
        WHERE 1=1
    '''
    params = []
    
    if search_query:
        query += " AND s.Name LIKE ?"
        params.append(f"%{search_query}%")
    if date_filter:
        query += " AND a.Date = ?"
        params.append(date_filter)
        
    query += " ORDER BY a.Date DESC, a.Time DESC"
    
    records = conn.execute(query, params).fetchall()
    conn.close()
    return records

def get_dashboard_stats():
    conn = get_db_connection()
    total_students = conn.execute('SELECT COUNT(*) FROM Student').fetchone()[0]
    today = datetime.now().strftime('%Y-%m-%d')
    present_today = conn.execute('SELECT COUNT(*) FROM Attendance WHERE Date = ?', (today,)).fetchone()[0]
    total_records = conn.execute('SELECT COUNT(*) FROM Attendance').fetchone()[0]
    conn.close()
    return total_students, present_today, total_records