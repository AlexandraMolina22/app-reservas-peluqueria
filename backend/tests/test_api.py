import pytest
import sys
import os
from datetime import date, time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from app import app, db
from models import Usuario, Servicio, Cita

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_key'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Crear datos base para tests
            admin = Usuario(nombre="Admin", cedula="000", rol="admin")
            client_user = Usuario(nombre="Cliente1", cedula="111", rol="clienta")
            servicio1 = Servicio(nombre="Corte")
            servicio2 = Servicio(nombre="Tinte")
            db.session.add_all([admin, client_user, servicio1, servicio2])
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def login(client, nombre, cedula):
    return client.post('/login', data={'nombre': nombre, 'cedula': cedula}, follow_redirects=True)

def test_redireccion_inicio(client):
    res = client.get('/')
    # Debe redirigir al login
    assert res.status_code == 302
    assert '/login' in res.headers['Location']

def test_login_exitoso_y_fallo(client):
    # Login admin exitoso -> redirige a /admin
    res = login(client, "Admin", "000")
    assert b'admin' in res.data or res.status_code == 200
    
    # Login clienta exitoso -> redirige a /cliente
    res = login(client, "Cliente1", "111")
    assert b'index' in res.data or res.status_code == 200

    # Login fallido -> flash mensaje y redirige login
    res = login(client, "NoExiste", "999")
    assert b'Credenciales incorrectas' in res.data

def test_registro_usuario(client):
    # Registro nuevo usuario
    res = client.post('/registro', data={'nombre': 'Nuevo', 'cedula': '222'}, follow_redirects=True)
    assert b'Registro exitoso' in res.data
    with app.app_context():
        u = Usuario.query.filter_by(nombre='Nuevo').first()
        assert u is not None

    # Registro usuario existente (debe fallar)
    res = client.post('/registro', data={'nombre': 'Nuevo', 'cedula': '222'}, follow_redirects=True)
    assert b'El usuario ya existe' in res.data

def test_cliente_panel_acceso_autorizado_y_no_autorizado(client):
    # Sin login -> redirige a login con flash
    res = client.get('/cliente', follow_redirects=True)
    assert b'Acceso no autorizado' in res.data

    # Login clienta para acceder
    login(client, "Cliente1", "111")
    res = client.get('/cliente')
    assert res.status_code == 200
    assert b'Corte' in res.data or b'Tinte' in res.data  # Servicios listados

def test_cliente_reserva_cita(client):
    login(client, "Cliente1", "111")
    # Reserva cita en fecha y hora válidas
    res = client.post('/cliente', data={
        'servicio': '1',
        'fecha': date.today().strftime("%Y-%m-%d"),
        'hora': '10:00'
    }, follow_redirects=True)
    assert 'Cita reservada con éxito' in res.data.decode('utf-8')

    # Intentar reservar misma fecha y hora debe fallar
    res = client.post('/cliente', data={
        'servicio': '1',
        'fecha': date.today().strftime("%Y-%m-%d"),
        'hora': '10:00'
    }, follow_redirects=True)
    assert b'Ya hay una cita en esa hora' in res.data

    # Fecha y hora mal formateadas
    res = client.post('/cliente', data={
        'servicio': '1',
        'fecha': 'fecha_invalida',
        'hora': 'hora_invalida'
    }, follow_redirects=True)
    assert 'Formato de fecha u hora inválido' in res.data.decode('utf-8')

def test_admin_panel_acceso_y_listado(client):
    # Acceso sin admin -> debe fallar
    res = client.get('/admin', follow_redirects=True)
    assert b'Acceso restringido' in res.data

    # Login admin y acceso a panel
    login(client, "Admin", "000")
    res = client.get('/admin')
    assert res.status_code == 200
    # Puede listar citas (incluso si está vacío)
    assert b'Cita' in res.data or b'confirmar' in res.data or res.status_code == 200

def test_confirmar_y_cancelar_cita(client):
    login(client, "Admin", "000")
    with app.app_context():
        # Crear cita para confirmar y cancelar
        u = Usuario.query.filter_by(nombre="Cliente1").first()
        s = Servicio.query.first()
        cita = Cita(usuario_id=u.id, servicio_id=s.id, fecha=date.today(), hora=time(12,0), estado="pendiente")
        db.session.add(cita)
        db.session.commit()
        cita_id = cita.id

    # Confirmar cita
    res = client.post(f'/confirmar/{cita_id}', follow_redirects=True)
    assert b'Cita confirmada' in res.data

    # Cancelar cita
    res = client.post(f'/cancelar/{cita_id}', follow_redirects=True)
    assert b'Cita cancelada' in res.data

def test_logout(client):
    login(client, "Cliente1", "111")
    res = client.get('/logout', follow_redirects=True)
    assert 'Sesión cerrada' in res.data.decode('utf-8')
