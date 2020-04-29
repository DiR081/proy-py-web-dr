# Importamos la Libreria Para Formularios
from wtforms import Form, HiddenField
# Importamos la Libreria Para Validaciones
from wtforms import validators
# Importamos los campos de Texto y Clave del Formulario
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
# Importamos manejo de campos Correo Email
from wtforms.fields.html5 import EmailField
# Importamos capacidad de Usar de models las funciones
from .models import User

# Funcion - Validador CUSTOM - Nombre CODI
def form_validador_codi(form, campo):
    if campo.data == 'CODI02' or campo.data == 'Codi':
        raise validators.ValidationError('El Usuario CODI no es permitido.')
# Funcion - Valida Trampa Tarro de Miel
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')


# Clase Login del Formulario Logueo
class LoginForm(Form):
    # Agregamos Atributos del Formulario (Entrada) :
    # username
    # password
    username = StringField('Usuario', [
                validators.length(min=4, max=20, message='Longuitud Nombre Usuario fuera de Rango!')
    ])
    password = PasswordField('Clave',[
                validators.Required()
    ])

# Clase Registro del Formulario  + Atributos
class RegistroForm(Form):
    # Los Atributos son :
    # Trampa Tarro de Miel
    # usuario
    # email
    # clave
    # confirm_clave
    # acepto
    # Metodo - Validador CUSTOM - Verifica Un nombre de Usuario el cual No debe Existir
    def valida_usuario(self, usuario):
        if User.get_by_username(usuario.data):
           raise validators.ValidationError('El Usuario ya existe.. ;)')
    # Metodo - Valida Un nombre de Correo - No debe Existir
    def valida_correo(self, correo):
        if User.get_by_correo(correo.data):
            raise validators.ValidationError('El Correo ya existe.. ;)')
    #
    honeypot = HiddenField("", [length_honeypot] )
    usuario = StringField('Username', [
            validators.length(min=4, max=100),
            validators.Required(message='Un Nombre por Favor.'),
            form_validador_codi,
            valida_usuario
    ])
    email = EmailField('Correo Electrónico', [
            validators.length(min=6, max=100),
            validators.Required(message='El Correo es requerido.'),
            validators.Email(message='Ingrese un Email Valido.'),
            valida_correo
    ])
    clave = PasswordField('Password', [
            validators.Required('La CLAVE es obligtoria.'),
            validators.EqualTo('confirm_clave', message='Verificar las Claves Ingresadas.')
    ])
    confirm_clave = PasswordField('Confirmar Clave')
    acepto = BooleanField('', [
            validators.DataRequired()
    ])
    # Metodo - Vamos a crear validación CUSTOM - Primero Evaluas las Propias de Validator y luego las Custom
    def validate(self):
        if not Form.validate(self):
            return False

        # Cusmtom Clave de 2 o más caracteres
        if len(self.clave.data) < 3:
            self.clave.errors.append('Clave muy Corta.')
            return False

        return True

# Clase Registro de Formularios Tareas
class TareaForm(Form):
    # Los Atributos son :
    # title
    # description
    title = StringField('Título', [
            validators.length(min=4, max=50, message='Título fuera de Rango'),
            validators.DataRequired(message='Campo Título obligatorio')
    ])
    description = TextAreaField('Descripción', [
            validators.DataRequired('Campo obligtorio')
            ], render_kw={'rows': 5})
