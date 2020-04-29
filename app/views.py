# Importa clase para trabajar
from flask import Blueprint
# Importa funcion que permite renderizar las paginas Webs
from flask import render_template, request, flash, redirect, url_for, abort
# Importa de Formulario
from .forms import LoginForm, RegistroForm, TareaForm
# Importa Constantes
from .consts import *
# Importa funcio creada de envio de Correos
from .email import mail_bienvenida
# Importamos la funcion Login de Usuarios - nuevas secciones
from flask_login import login_user, logout_user, login_required, current_user

# Importamos modelo
from .models import User, Task
from . import login_manager
# Crear Instancia PAGE -- Con dos Argumentos
page = Blueprint('page' , __name__)

# Funcion - Optener el usuario actual para validar seccion
@login_manager.user_loader
def load_user(id):
	return User.get_by_id(id)

# pagina custom Error404 No Found + adorno
@page.app_errorhandler(404)
def page_no_encontrada(error):
	return	render_template('errors/404.html') , 404

@page.route('/')
@login_required			# Solo permie usurios con sesion
def index():
	nombre_usario = load_user(current_user.id)
	return render_template('index.html' , title='T. Index', nombre_usario=nombre_usario, link_activo='index')

@page.route('/tareas')
@page.route('/tareas/<int:pagina>')
@login_required			# Solo permie usurios con sesion
def tareas(pagina=1, por_pagina=2):
	#mis_tareas = current_user.Task  # Sin Paginación
	paginacion = current_user.Task.paginate(page=pagina, per_page=por_pagina)
	mis_tareas = paginacion.items

	return render_template('task/list_tareas.html' , title='Tareas', tasks=mis_tareas,
							pagination=paginacion, page=pagina, link_activo='tareas')

@page.route('/tareas/show/<int:task_id>')
@login_required			# Solo permie usurios con sesion
def get_task(task_id):
	# Optener el Objeto de la BD
	tarea = Task.query.get_or_404(task_id)

	return render_template('/task/show.html' , title='Detalla Tarea', task=tarea)

@page.route('/logout')
def logout():
	logout_user()
	flash(LOGOUT)
	return redirect(url_for('.login'))

@page.route('/login', methods=['GET' , 'POST'])
def login():
	if current_user.is_authenticated:  				# Si Usurio Actual Autenticado
		return redirect(url_for('.tareas'))			# redirige a Tareas

	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate() :
		user = User.get_by_username(form.username.data)
		if user and user.verifica_clave(form.password.data):
			login_user(user)
			flash(LOGIN)
		else:
			# Login InCorrecto
			flash(LOGIN_ERROR , 'error')

		# print(form.username.data)
		# print(form.password.data)
		# print('Nueva Sección creada!')

	return render_template('auth/login.html' , title='Logueo' , form=form, link_activo='login')

@page.route('/registro', methods=['GET', 'POST'])
def registro():
	if current_user.is_authenticated:  				# Si Usurio Actual Autenticado
		return redirect(url_for('.tareas'))			# redirige a Tareas

	form = RegistroForm(request.form)

	if request.method == 'POST':
		if form.validate():
			usuarioCreado = User.create_element(form.usuario.data, form.clave.data, form.email.data)
			flash('Usuario Registrado Correctamente.')
			login_user(usuarioCreado)
			mail_bienvenida(usuarioCreado)
			return redirect(url_for('.tareas'))

	#print('Usurio Creado Correctamente!')
	#print(usuarioCreado.id)

	return render_template('auth/registroF.html', title='Registro de Usuarios',
							form=form, link_activo='registro')

@page.route('/tareas/nueva', methods=['GET', 'POST'])
@login_required
def new_task():
	form=TareaForm(request.form)

	if request.method == 'POST' and form.validate():
		task = Task.create_element(form.title.data, form.description.data, current_user.id)
		if task:
			flash(TASK_CREATED)

	return render_template('task/new.html', title='Nueva Tarea',
							form=form, link_activo='new_task')

@page.route('/tareas/editar/<int:task_id>',  methods=['GET','POST'])
@login_required
def editar_tarea(task_id):
	# Realizo la consulta según el id de la Tarea suministrado
	task = Task.query.get_or_404(task_id)
	# Solo Usuarios Dueños de la tarea la pueden editar
	if task.user_id != current_user.id:
		abort(404)
	# Ahora se pasa al formulario los valores del Objeto consultado
	form = TareaForm(request.form, obj=task)

	if request.method == 'POST' and form.validate():
		print('Confimo POST VIEWS.py')
		#print(form.description.data)
		desc = form.description.data	# Datos Obtenido del Formulario
		task = Task.actualiza_elemento(task.id, form.title.data, desc)
		if task:
			flash(TASK_UPDATED)

	return render_template('task/editar_tarea.html', title='Editar Tarea', form=form)

@page.route('/tareas/borrar/<int:task_id>')
@login_required
def borrar_tarea(task_id):
	tarea = Task.query.get_or_404(task_id)

	if tarea.user_id != current_user.id:
		abort(404)

	if Task.delete_element(tarea.id):
		flash(TASK_DELETED)

	return redirect(url_for('.tareas'))
