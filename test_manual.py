import requests
import json

# URL de tu API
url = 'http://127.0.0.1:5000/api/students'

# Datos del estudiante a crear
nuevo_estudiante = {
    "first_name": "Gustavo",
    "last_name": "Barreto",
    "email": "gustavo.barreto@unellez.edu.ve",
    "major": "Doctorado Educacion",
    "semester": 1,
    "gpa": 4.0,
    "enrollment_date": "2026-01-30"
}

print("1. Intentando crear estudiante...")
response = requests.post(url, json=nuevo_estudiante)

if response.status_code == 201:
    print("✅ ÉXITO: Estudiante creado!")
    print("Respuesta del servidor:", response.json())
else:
    print("❌ ERROR:", response.status_code)
    print(response.text)

print("\n2. Verificando si se guardó en la lista...")
response_get = requests.get(url)
print("Lista actual de estudiantes:", response_get.json())