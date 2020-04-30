# Importamos la funcion Crear_Apps
from app import crear_app
# Importamos el manejo a los Modelos
from app import db, User, Task

# Importa clase que permite levantar el servidor desde una clase, e interprete de Consola
from flask_script import Manager, Shell

# Importa Diccionario que permite levantar  Configuraciones en el servidor
from config import configDic

# Defino una Configuracion a usar del Diccionario
Config_class = configDic['development']

# Crear los parametros del shell
def mi_shell_context():
	# Retorna el Diccionario de los context y modelos - Aplicacion, DataBase y Modelos
	return dict(app=app, db=db, User=User, Task=Task)
# Obtener la aplicacion + Se envia Obj de Config
app = crear_app(Config_class)

# Clasica Condicion de Inicio
if __name__ == '__main__':
	#
	manager = Manager(app)
	# levantar utilidad Shell
	manager.add_command('shell', Shell(make_context=mi_shell_context) )
	manager.run()
