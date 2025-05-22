from flask import Flask
from flask_wtf import CSRFProtect  # ← Agregado
from database import db
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'frontend', 'templates')
    static_dir = os.path.join(base_dir, '..', 'frontend', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/peluqueria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'tu_clave_secreta_aqui'

    # Inicializar extensiones
    db.init_app(app)
    CSRFProtect(app)  # ← Protección CSRF activada

    return app

app = create_app()

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
