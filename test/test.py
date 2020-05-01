# Importamos - para prebas unitarias
import unittest

# Importamos trabajar con la APP de Flask
from flask import current_app

# Importamos Modulos y la funcion de cear apps
from app import crear_app
from app import db, User, Task

# Importamos de config lo necesario
from config import configDic

# Creamos la Clase de Pruebas heredando de unittest (TestCase)
class DemoTestCase(unittest.TestCase):
    # Función automatica al Iniciar la Clase
    def setUp(self):
        print('En DemoTestCase - Configuración Previa a la Ejecución.')
        config_class = configDic['test']
        self.app = crear_app(config_class)

        # Empujar el contexto de la APP
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.id = 1

    # Función automatica al terminar la Clase
    def tearDown(self):
        print('En DemoTestCase - Despues de la Ejecución.')
        # Limpiamos datos y session
        db.session.remove()
        db.drop_all()
        # Estallar el contexto de la APP
        self.app_context.pop()

    def test_demo(self):
        print('En DemoTestCase - 1.Demo.')
        self.assertTrue( 1 == 1 )

    def test_usurio_existe(self):
        print('En Clase DemoTestCase - 2.Usuario Existe.')
        usuario = User.get_by_id(self.id)
        self.assertTrue(usuario is None)

    def test_crear_usuario(self):
        print('En Clase DemoTestCase - 3.Crear Usuario.')
        usuario = User.create_element('usuarioEnTest', 'clave123', 'correo@mail.com')
        self.assertTrue( usuario.id == self.id )

    def test_vacio(self):
        print('En DemoTestCase - 4.Vacio.')
        pass
