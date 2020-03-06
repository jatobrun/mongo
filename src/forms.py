from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, Form, FormField, TextField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src import tabla_usuarios, tabla_estudios
from flask import session


class ColaboradoresForm(Form):
    colaborador = StringField(
        'Agrega un colaborador')
    revisar = SubmitField('Revisar colaborador')

    def validate_colaborador(self, colaborador):
        user = tabla_usuarios.find_one({'usuario': colaborador.data})
        if not(user):
            raise ValidationError('Este usuario no existe. Porfavor ingrese otro.')


class Registration_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme Contraseña', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Ingrese')

    def validate_username(self, username):
        user = tabla_usuarios.find_one({'usuario': username.data})
        if user:
            raise ValidationError(
                'Este usuario no esta disponibles. Porfavor ingrese otro.')

    def validate_email(self, email):
        email = tabla_usuarios.find_one({'email': email.data})
        if email:
            raise ValidationError(
                'Este email ya esta registrado. Porfavor inicie sesion o recupere su contraseña')


class LogIn_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('  Recordar mi usuario')
    submit = SubmitField('Inicia Sesion')


class UpdateAccount_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Actualiza tu foto de perfil',
                        validators=[FileAllowed(['jpg', 'png'])])
    colaboradores = FormField(ColaboradoresForm)
    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if session['user'] != username.data:
            user = tabla_usuarios.find_one({'usuario': username.data})
            if user:
                raise ValidationError(
                    'Este usuario no esta disponibles. Porfavor ingrese otro.')

    def validate_email(self, email):
        if session['email'] != email.data:
            email = tabla_usuarios.find_one({'email': email.data})
            if email:
                raise ValidationError(
                    'Este email ya esta registrado. Porfavor inicie sesion o recupere su contraseña')


class PostForm(FlaskForm):
    titulo = StringField('Titulo')
    nombre_paciente = StringField(
        'Nombre del paciente')
    apellido_paciente = StringField(
        'Apellido del paciente')
    edad = IntegerField('Edad del paciente')
    nombre_doctor = StringField(
        'Nombre del doctor')
    apellido_doctor = StringField(
        'Apellido del doctor')
    contenido = TextAreaField('Sintomas')
    diagnostico = TextAreaField('Diagnostico')
    comentarios = TextAreaField('Comentarios')
    archivo1 = FileField('Radiografia 1', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo2 = FileField('Radiografia 2', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo3 = FileField('Radiografia 3', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo4 = FileField('Radiografia 4', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo5 = FileField('Radiografia 5', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo6 = FileField('Tomografia1 DICOM', validators=[
        FileAllowed(['DCM', 'jpg', 'png', 'dcm'])])
    archivo7 = FileField('Tomografia2 DICOM', validators=[
        FileAllowed(['DCM', 'png', 'jpg', 'dcm'])])
    archivo8 = FileField('Tomografia3 DICOM', validators=[
        FileAllowed(['DCM', 'jpg', 'png', 'dcm'])])
    submit = SubmitField('Agregar Estudio')

class BuscadorForm(FlaskForm):
    token = StringField('Ingrese el codigo de tu estudio', validators=[DataRequired()])
    submit = SubmitField('Buscar estudio')
    def validate_token(self, token):
        estudio_token = tabla_estudios.find_one({'token': token.data})
        print(estudio_token)
        print(not(estudio_token))
        print('Se imprimio el token')
        if not(estudio_token):
            print('hola')
            raise ValidationError('Esta clave no existe. Porfavor ingrese otra.')

class Add_colaboradorForm(FlaskForm):
    l_colaborador = SelectField('Colaboradores')
    submit = SubmitField('Agregar Colaborador')