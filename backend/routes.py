from flask import render_template, request, redirect, url_for, session, flash
from app import app
from models import Usuario, Cita, Servicio
from database import db
from datetime import datetime

# Redirige '/' al login
@app.route('/')
def inicio():
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        usuario = Usuario.query.filter_by(nombre=nombre, cedula=cedula).first()
        
        if usuario:
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol
            if usuario.rol == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('cliente_panel'))
        else:
            flash('Credenciales incorrectas o usuario no registrado.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        usuario_existente = Usuario.query.filter_by(nombre=nombre, cedula=cedula).first()
        
        if usuario_existente:
            flash('El usuario ya existe. Por favor inicia sesión.', 'warning')
            return redirect(url_for('login'))

        nuevo_usuario = Usuario(nombre=nombre, cedula=cedula, rol='clienta')
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Inicia sesión para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

# Vista para clientas (index.html)
@app.route('/cliente', methods=['GET', 'POST'])
def cliente_panel():
    usuario_id = session.get('usuario_id')
    rol = session.get('rol')

    if not usuario_id or rol != 'clienta':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('login'))

    servicios = Servicio.query.all()
    
    if request.method == 'POST':
        servicio_id = request.form['servicio']
        fecha = request.form['fecha']
        hora = request.form['hora']

        # Convertir fecha y hora a objetos datetime para SQLite
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_obj = datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            flash('Formato de fecha u hora inválido.', 'danger')
            return redirect(url_for('cliente_panel'))
        
        cita_existente = Cita.query.filter_by(fecha=fecha_obj, hora=hora_obj).first()
        if cita_existente:
            flash('Ya hay una cita en esa hora. Elige otra.', 'warning')
            return redirect(url_for('cliente_panel'))

        nueva_cita = Cita(usuario_id=usuario_id, servicio_id=servicio_id,
                          fecha=fecha_obj, hora=hora_obj, estado="pendiente")
        db.session.add(nueva_cita)
        db.session.commit()
        flash('Cita reservada con éxito. Espera confirmación.', 'success')
        return redirect(url_for('cliente_panel'))
    
    # Obtener las citas del usuario para mostrarlas
    citas = Cita.query.filter_by(usuario_id=usuario_id).order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
    
    return render_template('index.html', servicios=servicios, citas=citas)

# Vista para administradora
@app.route('/admin')
def admin_panel():
    if session.get('rol') != 'admin':
        flash('Acceso restringido solo para la administradora.', 'danger')
        return redirect(url_for('login'))

    citas = Cita.query.all()
    return render_template('admin.html', citas=citas)

# Confirmar cita
@app.route('/confirmar/<int:cita_id>', methods=['POST'])
def confirmar_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    cita.estado = 'confirmada'
    db.session.commit()
    flash('Cita confirmada.', 'success')
    return redirect(url_for('admin_panel'))

# Cancelar cita
@app.route('/cancelar/<int:cita_id>', methods=['POST'])
def cancelar_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    cita.estado = 'cancelada'
    db.session.commit()
    flash('Cita cancelada.', 'info')
    return redirect(url_for('admin_panel'))

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))
