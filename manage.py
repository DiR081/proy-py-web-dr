# Importamos la funcion Crear_Apps
from app import crear_app
# Importamos el manejo a los Modelos
from app import db, User, Task

# Importa clase que permite levantar el servidor desde una clase, e interprete de Consola
from flask_script import Manager, Shell
# Importamos SQLAlquemy para trabajar con el migrate
from flask_sqlalchemy import SQLAlchemy
# Importamos la libreria de Migración
from flask_migrate import Migrate, MigrateCommand

# Importa Diccionario que permite levantar  Configuraciones en el servidor
from config import configDic

# Defino una Instancia con la Configuracion a usar en el APP definido en el Diccionario
Config_class = configDic['development']

# Crear los parametros del shell
def mi_shell_context():
	# Retorna el Diccionario de los context y modelos - Aplicacion, DataBase y Modelos
	return dict(app=app, db=db, User=User, Task=Task)
# Obtener la aplicacion + Se envia Obj de Config
app = crear_app(Config_class)
# Cremos la Instancia del Migrate
migrate = Migrate(app, db)

# Clasica Condicion de Inicio
if __name__ == '__main__':
	#
	manager = Manager(app)
	# Registramos un comando - utilidad Shell
	manager.add_command('shell', Shell(make_context=mi_shell_context) )
	# Registramos un comando - importar DataBase
	manager.add_command('db', MigrateCommand)
	# Comando Custom - test
	@manager.command
	def test():
		import unittest
		tests = unittest.TestLoader().discover('test')
		unittest.TextTestRunner().run(tests)
	# Arranca la APP
	manager.run()
