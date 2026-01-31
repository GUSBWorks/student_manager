from flask import Flask
from app.routes.student_routes import student_bp
from flasgger import Swagger

def create_app():
    """Application Factory Pattern to create the Flask app."""
    app = Flask(__name__)
    
    # 1. Swagger Visual configuration
    app.config['SWAGGER'] = {
        'title': 'Student Management API',
        'uiversion': 3,
        'description': 'API for the management of university students (CRUD) by: Gustavo Barreto, José Marcano and Gemini! :D'
    }
    
    # 2. Execute Swagger
    swagger = Swagger(app)
    
    # 3. Blueprint registering (the routes)
    app.register_blueprint(student_bp)
    
    return app



#----------------------------NO SWAGGER-------------------------#

# from flask import Flask
# from app.routes.student_routes import student_bp

# def create_app():
#     """Application Factory Pattern to create the Flask app."""
#     app = Flask(__name__)
    
#     # Register the blueprint (connect the routes)
#     app.register_blueprint(student_bp)
    
#     return app

# if __name__ == "__main__":
#     app = create_app()
#     # Run the application on port 5000
#     app.run(debug=True, port=5000)
    