from app import app
from database import db
from models import Usuario, Servicio

with app.app_context():
    db.create_all()

    if not Usuario.query.first():
        print("⚙️ Insertando usuarios...")
        admin = Usuario(nombre="Admin", cedula="1234", rol="admin")
        clienta = Usuario(nombre="Clienta1", cedula="5678", rol="clienta")
        db.session.add_all([admin, clienta])

    if not Servicio.query.first():
        print("⚙️ Insertando servicios...")
        servicios = ["Uñas", "Tintura", "Keratina", "Tratamiento capilar"]
        for nombre in servicios:
            db.session.add(Servicio(nombre=nombre))

    db.session.commit()
    print("✅ Base de datos inicializada con usuarios y servicios.")
