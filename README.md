# Sistema de Gestión de Estudiantes (API REST CRUD)

Backend de un sistema de gestión académica desarrollado con Python y Flask. Esta API permite administrar información de estudiantes (crear, leer, actualizar y eliminar) utilizando una base de datos SQLite.

## Requisitos Previos
* Python 3.13.5
* Flask 3.0.0

## Instalación y Ejecución

1. **Clonar el repositorio** (o descargar la carpeta):
   ```bash
   git clone <tu-link-del-repo>

2. Crear y activar entorno virtual (Opcional pero recomendado):
    python -m venv venv
    # En Windows:
        venv\Scripts\activate
    # En Mac/Linux:
        source venv/bin/activate

3. Instalar dependencias:
    pip install -r requirements.txt

4. Inicializar la Base de Datos:
    python app/database/init_db.py

5. Ejecutar el Servidor:
    python app/__init__.py

## Uso de la API (Endpoints)

      Método                   Endpoint                 Descripción                                       Ejemplo de Body (JSON)
        GET,                /api/students,          Listar todos los estudiantes,                                   N/A
        GET,                /api/students/<id>,     Ver detalle de un estudiante,                                   N/A
        POST,               /api/students,          Crear estudiante,                               "{ ""first_name"": ""Juan"", ... }"
        PUT,                /api/students/<id>,     Actualizar todo el estudiante,                  "{ ""first_name"": ""Pedro"", ... }"
        DELETE,             /api/students/<id>,     Borrar (lógico),                                                N/A

## USO DE IA

* Herramientas utilizadas:

Gemini 3.0

* Aplicación en el proyecto:

    1. Generación de estructura: Se utilizó IA para entender la organización de carpetas en Flask.

    2. Consultas SQL: Se solicitó ayuda para armar el CREATE TABLE con las restricciones correctas.

    3. Debugging: 

    - Error en el DELETE: solo daba validación de delete a traves del Swagger pero no ejecutaba la acción (el estudiante elimiando seguia estando en la tabla.)
    # Solucion:
    - Se le colocaron "Lentes" al controlador para que logrará distinguir entre los estudiantes inactivos y los cuales no, Gemini nos ayudo a resolverlo mejorando las funciones: get_all_students y get_student_by_id. (# CORRECCIÓN: Contamos solo los activos (is_active = 1) - # CORRECCIÓN: Traemos solo los activos)



* Adaptación del código:

El código generado por la IA fue revisado para asegurar que las variables usaran snake_case (Python) y que los comentarios estuvieran en inglés, cumpliendo con los estándares de la actividad.

* Cambios y optimizaciones realizadas con ayuda de la IA:

    - Cambio en la funcion get_all_students: Se realizó un cambio en la misma para añadir la paginación la cual antes no tenía, esto evita que el servidor colapse en caso de tener mucha cantidad de datos.
    - Cambio en la funcion get_students: Se realizó un cambio en la misma para que sea compatible con la paginación, al igualmente también se le añadio el codigo correspondiente a la documentación Swagger
    - Cambio en la función add_student: Se realizó un cambio en la misma para que sea compatible con la documentación Swagger.
    - Adición y Adaptación del código generado en la Parte B (José Marcano)

* Explicación de Codigo generado por IA:

    - init_db.py: Este codigo se encarga de la creación/inicialización de nuestra base de datos principal. //Funciones usados: create_table (SQLite), en caso tal de que la base ya este creada se usa una funcion if para el inicio automatico de la misma.

    - db_config.py: Este codigo se encarga de conectar la ruta de nuestra base de datos con las rutas y controladores previamente creados.

## Estándares de Codificación

* Idioma: Inglés (Variables, Funciones, Comentarios).

* Nomenclatura: snake_case por que usamos Python.

* Arquitectura: Separación de responsabilidades (Rutas, Controladores, Modelos).




