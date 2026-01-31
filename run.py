from app import create_app

# Creamos la aplicación usando la fábrica que definimos en __init__.py
app = create_app()

if __name__ == "__main__":
    # Arrancamos el servidor
    app.run(debug=True, port=5000)