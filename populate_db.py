import requests
import json

# Local URL API
url = 'http://127.0.0.1:5000/api/students'

# 10 student list for testing
students_list = [
    {"first_name": "Ana", "last_name": "Silva", "email": "ana.silva@university.edu", "major": "Medicine", "semester": 2, "gpa": 3.8, "enrollment_date": "2025-09-01"},
    {"first_name": "Carlos", "last_name": "Mendez", "email": "carlos.m@university.edu", "major": "Engineering", "semester": 5, "gpa": 3.5, "enrollment_date": "2024-03-15"},
    {"first_name": "Luisa", "last_name": "Rojas", "email": "luisa.r@university.edu", "major": "Law", "semester": 3, "gpa": 3.9, "enrollment_date": "2025-01-10"},
    {"first_name": "Jorge", "last_name": "Perez", "email": "jorge.p@university.edu", "major": "Education", "semester": 8, "gpa": 3.2, "enrollment_date": "2022-08-20"},
    {"first_name": "Maria", "last_name": "Gomez", "email": "maria.g@university.edu", "major": "Architecture", "semester": 4, "gpa": 3.7, "enrollment_date": "2024-09-05"},
    {"first_name": "Pedro", "last_name": "Diaz", "email": "pedro.d@university.edu", "major": "Computer Science", "semester": 1, "gpa": 4.0, "enrollment_date": "2026-01-15"},
    {"first_name": "Sofia", "last_name": "Hernandez", "email": "sofia.h@university.edu", "major": "Psychology", "semester": 6, "gpa": 3.6, "enrollment_date": "2023-04-12"},
    {"first_name": "Miguel", "last_name": "Torres", "email": "miguel.t@university.edu", "major": "Economics", "semester": 7, "gpa": 3.1, "enrollment_date": "2023-01-30"},
    {"first_name": "Laura", "last_name": "Castillo", "email": "laura.c@university.edu", "major": "Biology", "semester": 2, "gpa": 3.4, "enrollment_date": "2025-08-22"},
    {"first_name": "Andres", "last_name": "Vargas", "email": "andres.v@university.edu", "major": "Physics", "semester": 9, "gpa": 3.95, "enrollment_date": "2021-09-10"}
]

print("Loading data...")

for student in students_list:
    response = requests.post(url, json=student)
    if response.status_code == 201:
        print(f"✅ Registering: {student['first_name']} {student['last_name']}")
    elif response.status_code == 409:
        print(f"⚠️ Already exists (Duplicate email): {student['email']}")
    else:
        print(f"❌ Error registering {student['first_name']}: {response.text}")

print("\n✅ All data registered.")