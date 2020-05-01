# Importamos para el manejo del tiempo
import datetime
# Importamos la conexion SQLAlchemy desde la raiz del proyecto
from . import db
# Importamos capacidad Mixe de Funcion Login
from flask_login import UserMixin
# Importamos capacidad de Encriptar TEXTO (Claves) + Validar HASH
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

#Combertimos la Clase USER en un modelo SQLAlchemy, crea la tabla y sus campos(Columnas + Atributos)
class User(db.Model, UserMixin):
    __tablename__ = 'Usuarios'  # Cambio nombre de mi tabla

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(94), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now) # Sin () fix problem
    Task = db.relationship('Task', lazy='dynamic')          # Atributo para Relacion UNO a MUCHOS

    def verifica_clave(self, clave):
        return check_password_hash(self.encrypted_password, clave)

    @property
    def password(self):
        # Permite Retornar la propiedad PASSWORD sin valores para llamados externos
        pass

    @password.setter
    def password(self, valor):
        self.encrypted_password = generate_password_hash(valor)

    def __str__(self):
        return self.username

    # Nuevo metodo con Clase (cls + adorno) que (Crea los Ususarios en la DB)
    @classmethod
    def create_element(cls, username, password, email):
        user = User(username=username, password=password, email=email)

        db.session.add(user) # Agrego en la DB el Usuario
        db.session.commit()  # Confirmo los Cambios

        return user

    # Nuevo metodo con Clase para obtener los usuarios y Retornar
    @classmethod
    def get_by_username(cls, username):
        #print(User.query.filter_by(username=username).first())
        return User.query.filter_by(username=username).first()
    # Nuevo metodo con Clase para obtener los Correo y Retornar
    @classmethod
    def get_by_correo(cls, correo):
        return User.query.filter_by(email=correo).first()
    # Nuevo metodo con Clase para obtener User by ID
    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id=id).first()

class Task(db.Model):
    __tablename__ = 'tareas'
    # Mi propio metodo para reparar FIX en time Now()
    def tiempo_actual(self):
        print(datetime.datetime.now())
        return datetime.datetime.now()

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    create_at = db.Column(db.DateTime, default=tiempo_actual)
    update_at = db.Column(db.DateTime)

    # Creamos una propiedad que devuelve una descripcion corta de la tarea
    @property
    def descripcion_corta(self):
        if len(self.description) > 29:
            return self.description[0:28] + "..."
        return self.description

    @classmethod
    def create_element(cls, titulo, descripcion, usuario_id):
        task = Task(title=titulo, description=descripcion, user_id=usuario_id)

        db.session.add(task)
        db.session.commit()

        return task

    @classmethod
    def get_by_id(cls, id):
        print('ID Pasado ', id)
        return Task.query.filter_by(id=id).first()

    @classmethod
    def actualiza_elemento(cls, id, titulo, descripcion):
        tarea = Task.get_by_id(id)
        #print
        print(titulo)
        print(descripcion)

        if tarea is None:
            return False

        tarea.title = titulo
        tarea.description = descripcion

        db.session.add(tarea)
        db.session.commit()

        return tarea

    @classmethod
    def delete_element(cls, id):
        tarea = Task.get_by_id(id)

        if tarea is None:
            return False

        db.session.delete(tarea)
        db.session.commit()

        return True
