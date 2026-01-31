from flask import Flask
from app.routes.student_routes import student_bp

def create_app():
    """Application Factory Pattern to create the Flask app."""
    app = Flask(__name__)
    
    # Register the blueprint (connect the routes)
    app.register_blueprint(student_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    # Run the application on port 5000
    app.run(debug=True, port=5000)
    