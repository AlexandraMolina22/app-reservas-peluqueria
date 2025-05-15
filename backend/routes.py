from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from models import Usuario, Cita, Servicio
from database import db
from datetime import datetime

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        usuario = Usuario.query.filter_by(nombre=nombre, cedula=cedula).first()
        if usuario:
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol
            if usuario.rol == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('reservar'))
        else:
            return render_template('login.html', mensaje="Credenciales inválidas")
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')

        # Verificar si la cédula ya está registrada
        if Usuario.query.filter_by(cedula=cedula).first():
            return render_template('registro.html', mensaje="Cédula ya registrada")

        nuevo_usuario = Usuario(nombre=nombre, cedula=cedula, rol="clienta")
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        servicio_id = request.form.get('servicio')
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')

        usuario = Usuario.query.get(usuario_id)
        servicio = Servicio.query.get(servicio_id)

        if not servicio:
            return render_template('index.html', mensaje="Servicio no válido", servicios=Servicio.query.all(), usuario_id=usuario_id)

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            return render_template('index.html', mensaje="Fecha u hora inválida", servicios=Servicio.query.all(), usuario_id=usuario_id)

        # Validar que no haya ninguna cita en ese horario (sin importar servicio)
        cita_existente = Cita.query.filter_by(fecha=fecha, hora=hora).first()
        if cita_existente:
            return render_template('index.html', mensaje="Ya hay una cita en esa fecha y hora", servicios=Servicio.query.all(), usuario_id=usuario_id)

        nueva_cita = Cita(
            usuario_id=usuario.id,
            servicio_id=servicio.id,
            fecha=fecha,
            hora=hora
        )
        db.session.add(nueva_cita)
        db.session.commit()

        return render_template('index.html', mensaje="Cita reservada con éxito", servicios=Servicio.query.all(), usuario_id=usuario_id)

    servicios = Servicio.query.all()
    citas = Cita.query.filter_by(usuario_id=usuario_id).order_by(Cita.fecha, Cita.hora).all()
    return render_template('index.html', servicios=servicios, usuario_id=usuario_id, citas=citas)

@app.route('/admin')
def admin_panel():
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    citas = Cita.query.all()
    return render_template('admin.html', citas=citas)

@app.route('/admin/confirmar/<int:cita_id>', methods=['POST'])
def confirmar_cita(cita_id):
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    cita = Cita.query.get_or_404(cita_id)
    cita.estado = 'confirmada'
    db.session.commit()
    return redirect(url_for('admin_panel'))


@app.route('/admin/cancelar/<int:cita_id>', methods=['POST'])
def cancelar_cita(cita_id):
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    cita = Cita.query.get_or_404(cita_id)
    cita.estado = 'cancelada'
    db.session.commit()
    return redirect(url_for('admin_panel'))


@app.route('/api/citas')
def api_citas():
    if session.get('rol') != 'admin':
        return jsonify([]), 403
    citas = Cita.query.all()
    citas_list = []
    for c in citas:
        citas_list.append({
            "id": c.id,
            "nombre_clienta": c.usuario.nombre,
            "servicio": c.servicio.nombre,
            "fecha": c.fecha.strftime('%Y-%m-%d'),
            "hora": c.hora.strftime('%H:%M'),
            "estado": c.estado
        })
    return jsonify(citas_list)
