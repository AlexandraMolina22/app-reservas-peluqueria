from flask import render_template, request, redirect, url_for, session, flash
from app import app
from models import Usuario, Cita, Servicio
from database import db
from datetime import datetime
from forms import LoginForm, RegistroForm, ReservaForm  # importa los formularios


# Redirige '/' al login
@app.route('/')
def inicio():
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cedula = form.cedula.data
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

    return render_template('login.html', form=form)


# Registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cedula = form.cedula.data
        usuario_existente = Usuario.query.filter_by(nombre=nombre, cedula=cedula).first()
        
        if usuario_existente:
            flash('El usuario ya existe. Por favor inicia sesión.', 'warning')
            return redirect(url_for('login'))

        nuevo_usuario = Usuario(nombre=nombre, cedula=cedula, rol='clienta')
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Inicia sesión para continuar.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)


# Vista para clientas (index.html)
@app.route('/cliente', methods=['GET', 'POST'])
def cliente_panel():
    usuario_id = session.get('usuario_id')
    rol = session.get('rol')

    if not usuario_id or rol != 'clienta':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('login'))

    form = ReservaForm()
    # Llenar opciones para servicio
    servicios = Servicio.query.all()
    form.servicio.choices = [(s.id, s.nombre) for s in servicios]

    if form.validate_on_submit():
        servicio_id = form.servicio.data
        fecha_obj = form.fecha.data
        hora_obj = form.hora.data

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

    # Obtener las citas para mostrar
    citas = Cita.query.filter_by(usuario_id=usuario_id).order_by(Cita.fecha.desc(), Cita.hora.desc()).all()

    return render_template('index.html', form=form, citas=citas)

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
