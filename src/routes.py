from PIL import Image
import os
import time
import secrets
from flask import render_template, flash, redirect, url_for, session, request
from src.forms import Registration_Form, LogIn_Form, UpdateAccount_Form, PostForm, BuscadorForm, Add_colaboradorForm
from src import app, bcrypt, tabla_estudios, tabla_usuarios
# from flask_login import current_user, login_user
from bson.objectid import ObjectId
from math import ceil

# def acceso(template, title):
#     if 'user' in session:
#         return render_template(template, title=title, control_center=True)
#     else:
#         return redirect(url_for('login'))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = BuscadorForm()
    form2 = Add_colaboradorForm()
    if form.validate_on_submit():
        estudio = tabla_estudios.find_one({'token': form.token.data})
        print(estudio)
        return redirect(url_for('estudio', _id = estudio['_id']))
    return render_template('home.html', title='Home', form =form, legend = 'Holi', css=True, form2 = form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/historial")
def historial():
    if 'user' in session:
        limit = 1
        page = request.args.get('page', 1, type=int)
        starting_id = tabla_estudios.find(
            {'usuario': session['user']}).sort('_id', 1)
        count = tabla_estudios.count_documents({'usuario': session['user']})
        total_pages = ceil(count / limit)
        mitad = ceil(total_pages/2)
        hola = tabla_estudios.find_one({'usuario': session['user']})
        hola2 = tabla_estudios.find_one({'colaboradores': session['user']})
        estudios = []
        pages = []
        if hola or hola2:
            if page == 1 or page == total_pages:
                pages = []
                c = 0
                if mitad % 2 == 0:
                    print('impar')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
                else:
                    print('par')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
            else:
                pages = []
                c = 0
                for i in range(1, total_pages+1):
                    if c == 0 or c == total_pages-1 or c == page or c == page-1 or c == page-2:
                        pages.append(i)
                    else:
                        pages.append(None)
                    c += 1
                print(pages)
            last_id = starting_id[(page-1)*limit]['_id']
            estudios = tabla_estudios.find({'usuario': session['user'], '_id': {
                '$gte': last_id}}).sort('_id', 1).limit(limit)
            form = Add_colaboradorForm()
            form.l_colaborador.choices=[(colaborador, colaborador) for colaborador in tabla_usuarios.find_one({'usuario':session['user']})['colaboradores'][1:]]
            if form.validate.validate_on_submit():
                colaborador = form.l_colaborador.data
                tabla_estudios.update_one({'usuario': session['user']}, {'$set': {'colaboradores':colaborador}})

        if not(estudios):
            vacio_historial = True
        else: 
            vacio_historial = False
        return render_template('historial.html', title='Historial Clinico', control_center=True, estudios=estudios, css=True, pages=pages, current_page=page, vacio_historial = vacio_historial, form = form)
    else:
        return redirect(url_for('login'))


@app.route("/historial/new", methods=['GET', 'POST'])
def new():
    if 'user' in session:
        form = PostForm()
        if form.validate_on_submit():
            n_radiografias = 0
            n_tomografias = 0
            token = secrets.token_hex(3)
            if form.archivo1.data:
                archivo1, f_ext1 = save_picture(
                    form.archivo1.data, resize=False)
                n_radiografias += 1
            else:
                archivo1 = 'nada'
                f_ext1 = '.'
            if form.archivo2.data:
                archivo2, f_ext2 = save_picture(
                    form.archivo2.data, resize=False)
                n_radiografias += 1
            else:
                archivo2 = 'nada'
                f_ext2 = '.'
            if form.archivo3.data:
                archivo3, f_ext3 = save_picture(
                    form.archivo3.data, resize=False)
                n_radiografias += 1
            else:
                archivo3 = 'nada'
                f_ext3 = '.'
            if form.archivo4.data:
                archivo4, f_ext4 = save_picture(
                    form.archivo4.data, resize=False)
                n_radiografias += 1
            else:
                archivo4 = 'nada'
                f_ext4 = '.'
            if form.archivo5.data:
                archivo5, f_ext5 = save_picture(
                    form.archivo5.data, resize=False)
                n_radiografias += 1
            else:
                archivo5 = 'nada'
                f_ext5 = '.'
            if form.archivo6.data:
                archivo6, f_ext6 = save_picture(
                    form.archivo6.data, resize=False)
                n_tomografias += 1
            else:
                archivo6 = 'nada'
                f_ext6 = '.'
            if form.archivo7.data:
                archivo7, f_ext7 = save_picture(
                    form.archivo7.data, resize=False)
                n_tomografias += 1
            else:
                archivo7 = 'nada'
                f_ext7 = '.'
            if form.archivo8.data:
                archivo8, f_ext8 = save_picture(
                    form.archivo8.data, resize=False)
                n_tomografias += 1
            else:
                archivo8 = 'nada'
                f_ext8 = '.'
            estudio = {
                'usuario': session['user'],
                'creador': session['user'],
                'creador-imagen': session['image'],
                'titulo': form.titulo.data,
                'nombre_paciente': form.nombre_paciente.data,
                'apellido_paciente': form.apellido_paciente.data,
                'edad': form.edad.data,
                'nombre_doctor': form.nombre_doctor.data,
                'apellido_doctor': form.apellido_doctor.data,
                'contenido': form.contenido.data,
                'diagnostico': form.diagnostico.data,
                'comentarios': form.comentarios.data,
                'fecha': time.strftime("%d-%m-%Y"),
                'archivos': [(archivo1, '1', f_ext1), (archivo2, '2', f_ext2), (archivo3, '3', f_ext3), (archivo4, '4', f_ext4), (archivo5, '5', f_ext5), (archivo6, '6', f_ext6), (archivo7, '7', f_ext7), (archivo8, '8', f_ext8)],
                'token': token,
                'n_radiografia': n_radiografias,
                'n_tomografia': n_tomografias,
                'colaboradores': []
            }
            tabla_estudios.insert_one(estudio)
            flash('Estudio registrado correctamente', 'success')
            return redirect(url_for('new'))
        return render_template('create_post.html', title='Nuevo Estudio', control_center=True, form=form, css=True, legend='Nuevo Estudio')
    else:
        return redirect(url_for('login'))


@app.route("/consulta")
def consulta():
    if 'user' in session:
        return render_template('consulta.html', title='Consulta Virtual', control_center=True)
    else:
        return redirect(url_for('login'))


@app.route("/ia")
def ia():
    if 'user' in session:
        return render_template('ia.html', title='IA BETA', control_center=True)
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    login = LogIn_Form()
    if login.validate_on_submit():
        user = tabla_usuarios.find_one({'usuario': login.username.data})
        if user and bcrypt.check_password_hash(user['password'], login.password.data):
            # login_user(user, remember=login.remember.data)
            flash('Inicio de sesion completado satisfactoriamente', 'success')
            session['user'] = user['usuario']
            session['email'] = user['email']
            if user['image'] != None:
                session['image'] = user['image']
            else:
                session['image'] = 'default.jpg'
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(
                'No se pudo iniciar sesion, porfavor revise el usuario y contraseña', 'danger')
    return render_template('inicio_sesion.html', title='Inicio Sesion', form=login)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for('index'))
    register = Registration_Form()
    if register.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            register.password.data).decode('utf-8')
        usuario = {'usuario': register.username.data,
                   'password': hashed_pass, 'email': register.email.data, 'image': 'default.jpg', 'colaboradores': ['nada']}
        tabla_usuarios.insert_one(usuario)
        session['user'] = register.username.data
        session['email'] = register.email.data
        session['image'] = 'default.jpg'
        flash(
            f'Tu cuenta fue creada satisfactoriamente tu usuario es:{register.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', title='Registro', form=register)


def save_picture(form_picture, resize=True, tomografia=False):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if resize:
        picture_path = os.path.join(
            app.root_path, 'static/profile-pic', picture_fn)
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
    else:
        picture_path = os.path.join(
            app.root_path, 'static/estudio-pic', picture_fn)
        form_picture.save(picture_path)
    return picture_fn, f_ext


@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    if 'user' in session:
        profile = url_for('static', filename='profile-pic/'+session['image'])
        form = UpdateAccount_Form()
        if form.validate_on_submit():
            user = tabla_usuarios.find_one({'usuario': session['user']})
            colaboradores = user['colaboradores']
            if form.picture.data:
                if user['image'] != 'nada':
                    picture_path = os.path.join(
                        app.root_path, 'static/profile-pic', user['image'])
                    os.remove(picture_path)
                picture_file, _ = save_picture(form.picture.data)
                session['image'] = picture_file
            cambios = {'usuario': form.username.data,
                       'email': form.email.data, 'image': session['image']}
            tabla_usuarios.update_one(
                {'usuario': session['user']}, {'$set': cambios})
            if form.colaboradores.data:
                colaboradores.append(form.colaboradores.data['colaborador'])
                tabla_usuarios.update_one({'usuario': session['user']}, {
                                          '$set': {'colaboradores': colaboradores}})
            session['user'] = form.username.data
            session['email'] = form.email.data
            flash('Tus cambios se han actualizado', 'success')
            return redirect(url_for('perfil'))
        elif request.method == 'GET':
            form.username.data = session['user']
            form.email.data = session['email']
        usuario = tabla_usuarios.find_one({'usuario': session['user']})
        colaboradores = usuario['colaboradores']
        print(colaboradores)
        print(len(colaboradores))
        if colaboradores[0] == 'nada' and len(colaboradores)<=1:
            vacio_colaboradores = True
        else:
            vacio_colaboradores = False
            colaboradores = colaboradores[1:]
        return render_template('perfil.html', title='Perfil', control_center=True, profile=profile, form=form, css=True, colaboradores = colaboradores, vacio_colaboradores = vacio_colaboradores)
    else:
        return redirect(url_for('login'))


@app.route("/Index", methods=['GET', 'POST'])
def index():
    if 'user' in session:
        notificaciones = []
        if not(notificaciones):
            vacio_notificaciones = True
        else:
            vacio_notificaciones = False
        return render_template('notificaciones.html', title='Index', control_center=True, css=True, notificaciones = notificaciones, vacio_notificaciones = vacio_notificaciones)
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/historial/<_id>")
def estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    creador = tabla_usuarios.find_one({'usuario': estudio['usuario']})
    if 'user' in session:
        return render_template('estudio.html', title=estudio['titulo'], estudio=estudio, control_center=True, creador=creador, css=True)
    else:
        return render_template('estudio.html', title=estudio['titulo'], estudio = estudio, control_center = False, creador = creador, css = True)

@app.route("/historial/<_id>/update", methods=['GET', 'POST'])
def actualizar_estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    form = PostForm()
    if form.validate_on_submit():
        n_radiografias = 0
        n_tomografias = 0
        if form.archivo1.data:
            if estudio['archivos'][0][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][0][0])
                os.remove(picture_path)
            archivo1, f_ext1 = save_picture(form.archivo1.data, resize=False)
        else:
            archivo1, f_ext1 = estudio['archivos'][0][0], estudio['archivos'][0][2]
        if form.archivo2.data:
            if estudio['archivos'][1][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][1][0])
                os.remove(picture_path)
            archivo2, f_ext2 = save_picture(form.archivo2.data, resize=False)
        else:
            archivo2, f_ext2 = estudio['archivos'][1][0], estudio['archivos'][1][2]
        if form.archivo3.data:
            if estudio['archivos'][2][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][2][0])
                os.remove(picture_path)
            archivo3, f_ext3 = save_picture(form.archivo3.data, resize=False)
        else:
            archivo3, f_ext3 = estudio['archivos'][2][0], estudio['archivos'][2][2]
        if form.archivo4.data:
            if estudio['archivos'][3][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][3][0])
                os.remove(picture_path)
            archivo4, f_ext4 = save_picture(form.archivo4.data, resize=False)
        else:
            archivo4, f_ext4 = estudio['archivos'][3][0], estudio['archivos'][3][2]
        if form.archivo5.data:
            if estudio['archivos'][4][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][4][0])
                os.remove(picture_path)
            archivo5, f_ext5 = save_picture(form.archivo5.data, resize=False)
        else:
            archivo5, f_ext5 = estudio['archivos'][4][0], estudio['archivos'][4][2]
        if form.archivo6.data:
            if estudio['archivos'][5][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][5][0])
                os.remove(picture_path)
            archivo6, f_ext6 = save_picture(form.archivo6.data, resize=False)
        else:
            archivo6, f_ext6 = estudio['archivos'][5][0], estudio['archivos'][5][2]
        if form.archivo7.data:
            if estudio['archivos'][6][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][6][0])
                os.remove(picture_path)
            archivo7, f_ext7 = save_picture(form.archivo7.data, resize=False)
        else:
            archivo7, f_ext7 = estudio['archivos'][6][0], estudio['archivos'][6][2]
        if form.archivo8.data:
            if estudio['archivos'][7][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][7][0])
                os.remove(picture_path)
            archivo8, f_ext8 = save_picture(form.archivo8.data, resize=False)
        else:
            archivo8, f_ext8 = estudio['archivos'][7][0], estudio['archivos'][7][2]

        archivos = [(archivo1, '1', f_ext1), (archivo2, '2', f_ext2), (archivo3, '3', f_ext3), (archivo4, '4', f_ext4),
                    (archivo5, '5', f_ext5), (archivo6, '6', f_ext6), (archivo7, '7', f_ext7), (archivo8, '8', f_ext8)]
        for archivo in archivos:
            if archivo[0] != 'nada':
                if archivo[1] == '6' or archivo[1] == '7' or archivo[1] == '8':
                    n_tomografias += 1
                n_radiografias += 1
        cambios = {
            'usuario': session['user'],
            'titulo': form.titulo.data,
            'nombre_paciente': form.nombre_paciente.data,
            'apellido_paciente': form.apellido_paciente.data,
            'edad': form.edad.data,
            'nombre_doctor': form.nombre_doctor.data,
            'apellido_doctor': form.apellido_doctor.data,
            'contenido': form.contenido.data,
            'diagnostico': form.diagnostico.data,
            'comentarios': form.comentarios.data,
            'fecha': time.strftime("%d-%m-%Y"),
            'archivos': archivos,
            'n_radiografia': n_radiografias,
            'n_tomografia': n_tomografias
        }
        tabla_estudios.update_one(
            {'usuario': session['user']}, {'$set': cambios})
        flash('Cambios Realizados Satisfactoriamente!', 'success')
        return redirect(url_for('estudio', _id=estudio['_id']))
    elif request.method == 'GET':
        form.apellido_doctor.data = estudio['apellido_doctor']
        form.apellido_paciente.data = estudio['apellido_paciente']
        form.edad.data = estudio['edad']
        form.comentarios.data = estudio['comentarios']
        form.contenido.data = estudio['contenido']
        form.diagnostico.data = estudio['diagnostico']
        form.nombre_doctor.data = estudio['nombre_doctor']
        form.nombre_paciente.data = estudio['nombre_paciente']
        form.titulo.data = estudio['titulo']
        form.archivo1.data = estudio['archivos'][0][0]
        form.archivo2.data = estudio['archivos'][1][0]
        form.archivo3.data = estudio['archivos'][2][0]
        form.archivo4.data = estudio['archivos'][3][0]
        form.archivo5.data = estudio['archivos'][4][0]
        form.archivo6.data = estudio['archivos'][5][0]
        form.archivo7.data = estudio['archivos'][6][0]
        form.archivo8.data = estudio['archivos'][7][0]

    return render_template('create_post.html', title='Actualizar Estudio', control_center=True, form=form, css=True, legend='Actualizar Estudio')


@app.route("/historial/<_id>/delete", methods=['POST'])
def borrar_estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    tabla_estudios.delete_one({'_id': ObjectId(_id)})
    for archivo in estudio['archivos']:
        if archivo[0] != 'nada':
            picture_path = os.path.join(
                app.root_path, 'static/estudio-pic', archivo[0])
            os.remove(picture_path)
    return redirect(url_for('historial'))
