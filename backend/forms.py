from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cedula = StringField('Cédula', validators=[DataRequired()])

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cedula = StringField('Cédula', validators=[DataRequired()])

class ReservaForm(FlaskForm):
    servicio = SelectField('Servicio', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    hora = TimeField('Hora', format='%H:%M', validators=[DataRequired()])
