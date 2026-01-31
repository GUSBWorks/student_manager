# Student Management System API 🎓

A robust backend for university student academic management. Developed using **Python (Flask)** and **SQLite**, implementing RESTful architecture, strict validations, automated documentation, and containerization.

## ✨ Key Features

* **Complete CRUD:** Create, Read, Update, and Delete students.
* **Soft Delete & Restore:** Students are not permanently deleted; they are moved to a "recycle bin" and can be restored.
* **Pagination:** Optimized listing endpoint for handling large datasets.
* **Validations:** Strict control for unique emails, GPA range (0.0-4.0), and date formats.
* **Interactive Documentation:** Integrated with **Swagger UI** for visual API testing.
* **Dockerized:** Ready for containerized deployment.

## 📋 Prerequisites

* Python 3.13+
* Git
* Docker (Optional, for containerized execution)

## 🚀 Installation and Execution

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/GUSBWorks/student_manager.git
    cd student_manager
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    > **Tip:** If the command above fails or is not recognized, try this alternative: (it may occur in Windows 11)
    > ```bash
    > python -m pip install -r requirements.txt
    > ```

3.  **Initialize the Database:**
    ```bash
    python app/database/init_db.py
    ```
    *(This creates the `students.db` file with the required table).*

4.  **Load Test Data (Optional):**
    ```bash
    python populate_db.py
    ```
    *(Automatically inserts 10 dummy students for testing).*
    > **Note:** If this script returns errors (e.g., "IntegrityError" or duplicate emails), it means the database is already populated. You can safely ignore the error and proceed to the next step.

5.  **Start the Server:**
    ```bash
    python run.py
    ```

## 🐳 Running with Docker

The project includes configuration for containerized deployment, facilitating execution in any environment without manual dependency installation.

1.  **Build the image:**
    ```bash
    docker build -t student-manager .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 5000:5000 student-manager
    ```

The API will be available at `http://localhost:5000/api/students`.

## 🧪 Testing & Documentation (Swagger)

Once the server is running, visit the following URL to view the interactive documentation and test the endpoints:

👉 **http://127.0.0.1:5000/apidocs**

### Key Endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/students` | List students (Params: `page`, `per_page`, `is_active`). |
| `POST` | `/api/students` | Register a new student. |
| `GET` | `/api/students/<id>` | Get details of a specific student. |
| `PUT` | `/api/students/<id>` | Full update of student information. |
| `PATCH`| `/api/students/<id>` | Partial update (e.g., update only GPA). |
| `DELETE`| `/api/students/<id>` | Move to trash (Soft Delete). |
| `POST` | `/api/students/<id>/restore`| **[EXTRA]** Restore a deleted student. |

## 🚀 Quick Test Guide (Copy-Paste Examples)

To facilitate evaluation, here are exact JSON payloads to test each feature in **Swagger UI** or Postman.

### 1. List Students (GET)
* **Endpoint:** `/api/students`
* **Usage:** Get paginated list.
* **Parameters:**
    * `page`: 1
    * `per_page`: 5
    * `is_active`: true (set to `false` to view the recycle bin)

### 2. Create Student (POST)
* **Endpoint:** `/api/students`
* **Body (JSON):**
    ```json
    {
      "first_name": "Evaluator",
      "last_name": "Test",
      "email": "prof.test@university.edu",
      "major": "Computer Science",
      "semester": 1,
      "gpa": 4.0,
      "enrollment_date": "2026-02-01"
    }
    ```

### 3. Full Update (PUT)
* **Endpoint:** `/api/students/{id}` (Replace `{id}` with an actual ID, e.g., 1)
* **Body (JSON):**
    ```json
    {
      "first_name": "Evaluator",
      "last_name": "Updated",
      "email": "prof.update@university.edu",
      "major": "Education Masters",
      "semester": 2,
      "gpa": 3.8,
      "enrollment_date": "2026-02-01"
    }
    ```

### 4. Partial Update (PATCH)
* **Endpoint:** `/api/students/{id}`
* **Usage:** Ideal for correcting a single field without sending the whole object.
* **Body (JSON):**
    ```json
    {
      "gpa": 3.5
    }
    ```

### 5. Delete / Soft Delete (DELETE)
* **Endpoint:** `/api/students/{id}`
* **Effect:** The student disappears from the main list (`is_active=true`) but appears if filtering by `is_active=false`.

### 6. Restore Student (POST - Extra Feature)
* **Endpoint:** `/api/students/{id}/restore`
* **Usage:** Recover a student who was accidentally deleted.

---

## 🛠️ Troubleshooting Log

During development, we encountered and resolved several technical challenges. Below is a log of errors and their solutions:

### 1. Module Error (ModuleNotFoundError)
* **Error:** `ModuleNotFoundError: No module named 'flask'` when trying to execute `run.py`.
* **Cause:** The virtual environment did not have dependencies installed or was not activated.
* **Solution:** Created `requirements.txt` and executed `pip install -r requirements.txt`.

### 2. Package Structure (ImportError)
* **Error:** `ImportError: attempted relative import with no known parent package` when executing `python app/routes/student_routes.py`.
* **Cause:** Python did not recognize the `app` folder as a package because a submodule was being executed directly.
* **Solution:** Implemented `run.py` at the project root to import the app correctly as a module (`from app import create_app`) and ensured `__init__.py` files existed in every subfolder.

### 3. Data Persistence (Database Not Found)
* **Error:** The application ran, but the database reset itself or couldn't find the `students` table.
* **Cause:** `students.db` was generated in the root, but the code expected it inside `app/database/`.
* **Solution:** Adjusted configuration in `db_config.py` to use absolute paths (`os.path.join`) ensuring the database is always read from `app/database/students.db`.

### 4. Soft Delete Logic (Visual Persistence)
* **Error:** When deleting a student (`DELETE`), the server responded "Success", but the student still appeared in the general list (`GET`).
* **Cause:** The `get_all_students` function retrieved all records from the table without checking their status.
* **Solution:** Modified the SQL query to include the filter `WHERE is_active = 1` by default, hiding records marked as deleted.

### 5. Git Identity Unknown
* **Error:** Git failed on the first commit with the message `Please tell me who you are`.
* **Solution:** Configured global user credentials (`git config --global user.email ...`) to correctly sign changes.

---

## 🔄 Code Evolution (Refactoring)

The code evolved to support new features and improve scalability:

1.  **Initial Version (V1):**
    * Executed simple `SELECT * FROM students`.
    * *Issue:* Not scalable. Retrieving all records at once is inefficient for large datasets.

2.  **Paginated Version (V2):**
    * Added `page` and `per_page` parameters.
    * Implemented mathematical logic for SQL `LIMIT` and `OFFSET`.
    * *Improvement:* Allows retrieving data in chunks (e.g., 10 at a time).

3.  **Final Version with Filters (V3):**
    * Added `is_active` parameter.
    * Implemented dynamic logic to filter between "Active" and "Trash".
    * *Result:* A single function now handles normal listing, pagination, and viewing deleted files.

**Additional Innovation: Restore System**
Beyond basic requirements, we realized a "Soft Delete" is incomplete if it cannot be undone. We developed an exclusive endpoint `POST /api/students/<id>/restore` that allows "reviving" a deleted record by changing its `is_active` status from `0` to `1`.

---

## 🤖 AI Usage 

In accordance with the activity guidelines, the use of Generative AI tools is documented below:

**AI Tools Used:**
* Gemini 3.0 (Programming Assistant).

**Application in the Project:**
1.  **Project Structure:** AI suggested the modular folder architecture (separating `controllers`, `routes`, and `models`) to keep the code clean and scalable.
2.  **Dynamic SQL Queries:** AI was used to generate the logic for partial updates (`PATCH`) and dynamic filtering of active/inactive students using raw SQL.
3.  **Debugging:** Assistance in initial Flask configuration and fixing circular import errors in Python.

**Human Adaptation and Improvement:**
* The code generated by AI was refactored to comply with the required `snake_case` naming convention.
* Logic for **Restore** and **Regex Validations** was manually implemented, as it was not part of the AI's original scope.
* All comments and variables were translated and adapted to technical English.

## 📝 Coding Standards
* **Language:** Python (Flask).
* **Database:** Native SQLite (no ORM) to demonstrate SQL proficiency.
* **Style:** PEP 8, `snake_case` for functions/variables, Full English.

---
**Developed by:** Gustavo Barreto & José Marcano & Gemini.




## ESPAÑOL

# Student Management System API 🎓

Backend robusto para la gestión académica de estudiantes universitarios. Desarrollado con **Python (Flask)** y **SQLite**, implementando arquitectura RESTful, validaciones estrictas y documentación automática.

## ✨ Características Principales

* **CRUD Completo:** Crear, Leer, Actualizar y Eliminar estudiantes.
* **Soft Delete & Restore:** Los estudiantes no se borran permanentemente; van a una "papelera" y pueden ser restaurados.
* **Paginación:** Endpoint de listado optimizado para grandes volúmenes de datos.
* **Validaciones:** Control estricto de Emails únicos, GPA (0.0-4.0) y formatos de fecha.
* **Documentación Interactiva:** Integración con **Swagger UI** para probar la API visualmente.
* **Dockerizado:** Listo para desplegar en contenedores.

## 📋 Requisitos Previos

* Python 3.13+
* Git
* Docker (Optional, for containerized execution)

## 🚀 Instalación y Ejecución

## Instalacion Manual

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/GUSBWorks/student_manager.git
    cd student_manager
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    > **Sugerencia:** Si el comando anterior falla o no se reconoce, prueba esta alternativa: (suele ocurrir en Windows 11)
    > ```bash
    > python -m pip install -r requirements.txt
    > ```

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
    > **Nota**: Si este script devuelve errores (p. ej., "IntegrityError" o correos electrónicos duplicados), significa que la base de datos ya está llena. Puede ignorar el error y continuar con el siguiente paso.

5.  **Iniciar el Servidor:**
    ```bash
    python run.py
    ```

## 🧪 Pruebas y Documentación (Swagger)

Una vez iniciado el servidor, visita la siguiente URL para ver la documentación interactiva y probar los endpoints:

👉 **http://127.0.0.1:5000/apidocs**


## 🐳 Deployment con Docker

El proyecto incluye configuración para ser desplegado en contenedores, facilitando su ejecución en cualquier entorno sin instalar dependencias manualmente.

1.  **Construir la imagen:**
    ```bash
    docker build -t student-manager .
    ```

2.  **Ejecutar el contenedor:**
    ```bash
    docker run -p 5000:5000 student-manager
    ```

La API estará disponible en `http://localhost:5000/api/students`.

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



