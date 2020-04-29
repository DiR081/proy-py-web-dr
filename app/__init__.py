# Patron de diseño Single Thom
# Importamos la Clase necesaria e Indispensable FLASK
from flask import Flask
# Importamos la Clase necesaria
from flask_bootstrap import Bootstrap
#Importar Protenccion contra ataques CSRF  de la class
from flask_wtf.csrf import CSRFProtect
#Importamos capacidad de trabajar con SQL
from flask_sqlalchemy import SQLAlchemy
# Importamos herramientas para Logearnos
from flask_login import LoginManager
# Importamos capacidad de manejo Correos
from flask_mail import Mail
# Importa Constantes
from .consts import *

# Nuestra Instancia Flask y con algumento el contexo
app = Flask(__name__)
# Cargamos la Instancia
bootstrap = Bootstrap()
# Definimos la Instancia
csrf = CSRFProtect()
# Definimos la Instancia de la Base de Datos
db = SQLAlchemy()
# Instancia de Logueo
login_manager = LoginManager()
# Instancia para el Correo
mail = Mail()

# Para vincular las paginas e Instancias
from .views import page
# vincular Y crear las Tablas de DB
from .models import User

# Funcion que retorna la Instancia creada, que Arranca el servidor
#  Se recive Obj de Configuraciones
def crear_app(Obj_Configuraciones):
	app.config.from_object(Obj_Configuraciones)

	#print ('Hola, Inicia el servidor')
	mail.init_app(app)
	csrf.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = '.login'  # Redirecciona usuarios sin sesión
	login_manager.login_message = LOGIN_REQUIRED

	app.register_blueprint(page)
	# Crea contexto de la DB
	with app.app_context ():
		db.init_app(app)
		db.create_all()

	return app
