from flask import Flask
from database import db
import os

def create_app():
    # Obtener la ruta absoluta del directorio actual
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Definir las rutas absolutas para las carpetas de templates y static
    template_dir = os.path.join(base_dir, '..', 'frontend', 'templates')
    static_dir = os.path.join(base_dir, '..', 'frontend', 'static')

    # Crear la instancia de Flask con las rutas personalizadas
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/peluqueria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'tu_clave_secreta_aqui'  # necesario para sesiones

    # Inicializar la base de datos con la aplicación
    db.init_app(app)

    return app

# Crear la aplicación
app = create_app()

# Importar las rutas después de crear la aplicación para evitar dependencias circulares
from routes import *

if __name__ == "__main__":
    app.run(debug=True)