import pytest
import sys
import os
from datetime import date, time

# Establecer directorio base (carpeta backend)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from app import app, db
from models import Usuario, Servicio, Cita

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_crear_usuario(client):
    with app.app_context():
        usuario = Usuario(nombre="Laura", cedula="123456789", rol="clienta")
        db.session.add(usuario)
        db.session.commit()

        u = Usuario.query.filter_by(cedula="123456789").first()
        assert u is not None
        assert u.nombre == "Laura"

def test_crear_servicio(client):
    with app.app_context():
        servicio = Servicio(nombre="Corte de cabello")
        db.session.add(servicio)
        db.session.commit()

        s = Servicio.query.filter_by(nombre="Corte de cabello").first()
        assert s is not None
        assert s.nombre == "Corte de cabello"

def test_crear_cita(client):
    with app.app_context():
        usuario = Usuario(nombre="Juan", cedula="987654321", rol="clienta")
        servicio = Servicio(nombre="Tinte")
        db.session.add_all([usuario, servicio])
        db.session.commit()

        cita = Cita(usuario_id=usuario.id, servicio_id=servicio.id, fecha=date.today(), hora=time(10, 30))
        db.session.add(cita)
        db.session.commit()

        c = Cita.query.first()
        assert c is not None
        assert c.usuario_id == usuario.id
        assert c.servicio_id == servicio.id
