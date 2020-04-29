# Importamos la funcion Crear_Apps
from app import crear_app

# Importa clase que permite levantar el servidor desde una clase
from flask_script import Manager

# Importa Diccionario que permite levantar  Configuraciones en el servidor
from config import configDic

# Defino una Configuracion a usar del Diccionario
Config_class = configDic['development']

# Obtener la aplicacion + Se envia Obj de Config
app = crear_app(Config_class)

# Clasica Condicion de Inicio
if __name__ == '__main__':
	manager = Manager(app)
	manager.run()
