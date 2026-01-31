# Student Management System API 🎓

Backend robusto para la gestión académica de estudiantes universitarios. Desarrollado con **Python (Flask)** y **SQLite**, implementando arquitectura RESTful, validaciones estrictas y documentación automática.

## ✨ Características Principales

* **CRUD Completo:** Crear, Leer, Actualizar y Eliminar estudiantes.
* **Soft Delete & Restore:** Los estudiantes no se borran permanentemente; van a una "papelera" y pueden ser restaurados.
* **Paginación:** Endpoint de listado optimizado para grandes volúmenes de datos.
* **Validaciones:** Control estricto de Emails únicos, GPA (0.0-4.0) y formatos de fecha.
* **Documentación Interactiva:** Integración con **Swagger UI** para probar la API visualmente.

## 📋 Requisitos Previos

* Python 3.13+
* Git

## 🚀 Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone <tu-link-del-repo>
    cd student_manager
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicializar la Base de Datos:**
    ```bash
    python app/database/init_db.py
    ```
    *(Esto creará el archivo `students.db` con la tabla necesaria).*

4.  **Cargar datos de prueba (Opcional):**
    ```bash
    python populate_db.py
    ```
    *(Inserta 10 estudiantes automáticamente para pruebas).*

5.  **Iniciar el Servidor:**
    ```bash
    python run.py
    ```

## 🧪 Pruebas y Documentación (Swagger)

Una vez iniciado el servidor, visita la siguiente URL para ver la documentación interactiva y probar los endpoints:

👉 **http://127.0.0.1:5000/apidocs**

### Endpoints Clave:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/students` | Listar estudiantes (Params: `page`, `per_page`, `is_active`). |
| `POST` | `/api/students` | Registrar nuevo estudiante. |
| `GET` | `/api/students/<id>` | Obtener detalle de un estudiante. |
| `PUT` | `/api/students/<id>` | Actualización completa. |
| `PATCH`| `/api/students/<id>` | Actualización parcial (ej: solo GPA). |
| `DELETE`| `/api/students/<id>` | Enviar a papelera (Soft Delete). |
| `POST` | `/api/students/<id>/restore`| Restaurar estudiante eliminado. |

## 🚀 Guía de Pruebas Rápida (Ejemplos Copy-Paste)

Para facilitar la prueba de la API, aquí tiene los ejemplos exactos para probar cada funcionalidad en **Swagger UI** (`/apidocs`) o Postman.

### 1. Listar Estudiantes (GET)
* **Endpoint:** `/api/students`
* **Uso:** Obtiene la lista paginada.
* **Parámetros:**
    * `page`: 1
    * `per_page`: 5
    * `is_active`: true (poner `false` para ver la papelera)

### 2. Crear Estudiante (POST)
* **Endpoint:** `/api/students`
* **Body (JSON) para copiar:**
    ```json
    {
      "first_name": "Evaluador",
      "last_name": "Test",
      "email": "profesor.test@unellez.edu.ve",
      "major": "Ingeniería en Informática",
      "semester": 1,
      "gpa": 4.0,
      "enrollment_date": "2026-02-01"
    }
    ```

### 3. Actualizar Estudiante Completo (PUT)
* **Endpoint:** `/api/students/{id}` (Reemplace `{id}` por el ID creado, ej: 1)
* **Body (JSON) para copiar:**
    ```json
    {
      "first_name": "Evaluador",
      "last_name": "Actualizado",
      "email": "profesor.update@unellez.edu.ve",
      "major": "Maestría en Educación",
      "semester": 2,
      "gpa": 3.8,
      "enrollment_date": "2026-02-01"
    }
    ```

### 4. Actualizar Parcial (PATCH)
* **Endpoint:** `/api/students/{id}`
* **Uso:** Ideal para corregir solo un dato sin enviar todo el objeto.
* **Body (JSON) para copiar:**
    ```json
    {
      "gpa": 3.5
    }
    ```

### 5. Eliminar / Enviar a Papelera (DELETE)
* **Endpoint:** `/api/students/{id}`
* **Efecto:** El estudiante desaparece de la lista principal (`is_active=true`) pero aparece si filtra por `is_active=false`.

### 6. Restaurar Estudiante (POST - Feature Extra)
* **Endpoint:** `/api/students/{id}/restore`
* **Uso:** Recupere un estudiante que fue eliminado accidentalmente.
* **Prueba:**
    1. Elimine un ID (ej: 1).
    2. Verifique que da 404 en el GET normal.
    3. Ejecute este endpoint `/api/students/1/restore`.
    4. El estudiante vuelve a aparecer en la lista activa.



## 🤖 Uso de IA

De acuerdo con los lineamientos de la actividad, se documenta el uso de herramientas de Inteligencia Artificial Generativa:

**Herramientas IA utilizadas:**
* Gemini 3.0 (Asistente de Programación).

**Aplicación en el proyecto:**
1.  **Estructura del Proyecto:** La IA sugirió la arquitectura de carpetas modular (separando `controllers`, `routes` y `models`) para mantener el código limpio y escalable.
2.  **Consultas SQL Dinámicas:** Se utilizó IA para generar la lógica de actualización parcial (`PATCH`) y el filtrado dinámico de estudiantes activos/inactivos en SQL puro.
3.  **Debugging:**  Asistencia en la configuración inicial de Flask y corrección de errores de importación circular en Python. Entrando más en detalle abajo.

## 🛠️ Bitácora de Errores y Soluciones (Troubleshooting & Debugging)

Durante el desarrollo, nos enfrentamos a varios desafíos técnicos. A continuación, se detallan los errores encontrados y las soluciones implementadas, demostrando el proceso de depuración y de aprendizaje:

### 1. Error de Módulos (ModuleNotFoundError)
* **Error:** `ModuleNotFoundError: No module named 'flask'` al intentar ejecutar `run.py`.
* **Causa:** El entorno virtual no tenía las dependencias instaladas o no estaba activado.
* **Solución:** Se creó un archivo `requirements.txt` y se ejecutó `pip install -r requirements.txt`.

### 2. Estructura de Paquetes (ImportError)
* **Error:** `ImportError: attempted relative import with no known parent package` al ejecutar `python app/routes/student_routes.py`.
* **Causa:** Python no reconocía la carpeta `app` como un paquete porque se intentaba ejecutar un submódulo directamente.
* **Solución:** Se implementó el archivo `run.py` en la raíz del proyecto para importar la aplicación correctamente como un módulo (`from app import create_app`) y se aseguraron los archivos `__init__.py` en cada subcarpeta.

### 3. Persistencia de Datos (Database Not Found)
* **Error:** La aplicación funcionaba pero la base de datos se reiniciaba o no encontraba la tabla `students`.
* **Causa:** El archivo `students.db` se generaba en la raíz pero el código lo buscaba dentro de `app/database/`.
* **Solución:** Se ajustó la configuración en `db_config.py` para usar rutas absolutas (`os.path.join`) y asegurar que la base de datos siempre se lea desde `app/database/students.db`.

### 4. Lógica de Soft Delete (Persistencia Visual)
* **Error:** Al eliminar un estudiante (`DELETE`), el servidor respondía "Éxito", pero el estudiante seguía apareciendo en el listado general (`GET`).
* **Causa:** La función `get_all_students` traía todos los registros de la tabla sin discriminar su estado.
* **Solución:** Se modificó la consulta SQL para incluir el filtro `WHERE is_active = 1` por defecto, ocultando los registros marcados como eliminados.

### 5. Git Identity Unknown
* **Error:** Git fallaba al intentar hacer el primer commit con el mensaje `Please tell me who you are`.
* **Solución:** Se configuraron las credenciales globales de usuario y correo (`git config --global user.email ...`) para firmar los cambios correctamente.

**Adaptación y Mejora Humana:**
* El código generado por la IA fue refactorizado para cumplir con la nomenclatura `snake_case` exigida.
* Se implementó manualmente la lógica de **Restauración (Restore)** y **Validaciones Regex**, que no estaban en el alcance original sugerido por la IA.
* Se tradujeron y adaptaron todos los comentarios y variables al inglés técnico requerido.

## Evolución del Código (Refactorización)

El código no fue estático; evolucionó para soportar nuevas funcionalidades. Un ejemplo clave fue la función `get_all_students` en el controlador:

1.  **Versión Inicial (V1):**
    * Simplemente ejecutaba `SELECT * FROM students`.
    * *Problema:* No escalable. Si hay 1000 estudiantes, trae los 1000.

2.  **Versión Paginada (V2):**
    * Se añadieron parámetros `page` y `per_page`.
    * Se implementó lógica matemática para `LIMIT` y `OFFSET`.
    * *Mejora:* Permite traer datos por bloques (ej: de 10 en 10).

3.  **Versión Final con Filtros (V3):**
    * Se añadió el parámetro `is_active`.
    * Se implementó lógica dinámica para filtrar entre "Activos" y "Inactivos".
    * *Resultado:* Una sola función ahora maneja listado normal, paginación y visualización de archivos eliminados.

**Innovación Adicional: Sistema de Restauración**
Más allá de los requisitos básicos, notamos que un "Soft Delete" (Borrado Lógico) está incompleto si no se puede deshacer. Desarrollamos un endpoint exclusivo `POST /api/students/<id>/restore` que permite "revivir" un registro eliminado cambiando su estado `is_active` de `0` a `1`, proporcionando una red de seguridad completa para el usuario.

## 📝 Estándares de Codificación
* **Lenguaje:** Python (Flask).
* **Base de Datos:** SQLite nativo (sin ORM) para demostrar dominio de SQL.
* **Estilo:** PEP 8, `snake_case` para funciones/variables, Full English.

---
**Desarrollado por:** Gustavo Barreto & José Marcano & Gemini.



