# Importamos - para prebas unitarias
import unittest

# Importamos trabajar con la APP de Flask
from flask import current_app

# Importamos Modulos y la funcion de cear apps
from app import crear_app
from app import db, User, Task

# Creamos la Clase de Pruebas heredando de unittest (TestCase)
class DemoTestCase(unittest.TestCase):
    # funciones
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_demo(self):
        self.assertTrue( 1 == 1 )
